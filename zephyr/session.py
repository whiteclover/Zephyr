#!/usr/bin/env python
#
# Copyright 2015-2016 zephyr
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from functools import wraps
import uuid

from tornado.escape import json_encode, json_decode
from zephyr import pedis
from zephyr.breeze import Model
from zephyr.util import lazy_attr


USER = 'user'
ROOT = 'root'
ADMIN = 'administrator'
EDITOR = 'editor'


class Account(object):

    STATUSES = {
        'active': 'active',
        'inactive': 'inactive',
    }

    USER = 'user'
    ROOT = 'root'
    ADMIN = 'administrator'
    EDITOR = 'editor'
    ROLES = {
        # 'root' : 'root',
        'administrator': 'administrator',
        'editor': 'editor',
        'user': 'user'
    }

    def __init__(self, uid, session_id, role, name, email, remote_ip):
        self.uid = uid
        self.session_id = session_id
        self.role = role
        self.name = name
        self.email = email
        self.remote_ip = remote_ip

    def inactive(self):
        return self.status == 'inactive'

    def is_guest(self):
        return self.uid == 0

    def is_root(self):
        return self.uid == 1

    def is_admin(self):
        return self.role == self.ADMIN

    def is_editor(self):
        return self.role == self.EDITOR

    def is_login(self):
        return self.uid != 0

    @lazy_attr
    def sessionID(self):
        return SessionID(self.uid, self.session_id)

    def toAuthor(self):
        return Author(self.uid, self.name)

    def __json__(self):
        return self.__dict__

    @staticmethod
    def fromUser(user):
        return Account(user.uid, None, user.role, user.username, user.email, None)


class Author(object):

    def __init__(self, uid, name):
        self.uid = uid
        self.name = name

    def avator(self):
        pass

    def wigget(self):
        pass


class SessionID(object):

    def __init__(self, uid, session_id):
        self.uid = uid
        self.session_id = session_id

    @staticmethod
    def fromSession(session):
        if session is None:
            return None
        uid, session_id = session.split(':', 1)
        uid = int(uid)
        return SessionID(uid, session_id)

    def __str__(self):
        return '%d:%s' % (self.uid, self.session_id)


class SessionManager(object):

    any_user = {

        'uid': 0,
        'name': 'anyoms',
        'role': "none",
        'email': None,

    }

    def __init__(self, request):
        self.request = request

    def logout(self):
        request = self.request

        redis = pedis.db()

        redis.delete('session:' + str(request.account.sessionID))
        self.request.clear_cookie('session')
        request.account = None

    def loadByUser(self, user):
        redis = pedis.db()
        request = self.request
        session = self.genSessionID(user.uid)

        json = {
            'uid': user.uid,
            'name': user.username,
            'email': user.email,
            'role': user.role
        }

        session_id = str(session)

        redis.setex('session:' + session_id, json_encode(json), 24 * 60 * 60)
        redis.delete('session:' + str(request.account.sessionID))
        request.set_secure_cookie('session', session_id)

        request.account = Account(json['uid'],  session.session_id, json['role'], json['name'], json['email'], request.remote_ip)

    def loadByRequest(self):
        redis = pedis.db()
        request = self.request
        session = SessionID.fromSession(request.get_secure_cookie('session'))

        json = None
        if session is not None:
            data = redis.get('session:' + str(session))
            if data:
                try:
                    json = json_decode(data)
                except:
                    pass

        if json is None:

            json = self.any_user
            session = self.genSessionID(json['uid'])
            session_id = str(session)
            redis.setex('session:' + session_id, json_encode(json), 30 * 60)
            request.set_secure_cookie('session', session_id)

        request.account = Account(json['uid'],  session.session_id, json['role'], json['name'], json['email'], request.remote_ip)

    def genSessionID(self, uid):
        session_id = str(uuid.uuid4())
        return SessionID(uid, session_id)


from zephyr.breeze import Handler

def security(role='guest'):
    def decorator(f):
        @wraps(f)
        def _decorator(self, *args, **kw):
            me = self.account
            if me.is_guest() and request.path != '/login':
                return self.redirect(self.revserve_url('login'))
            access = False
            if me.is_root():
                access = True
            elif me.inactive():
                access = False
            elif me.role == role:
                access = True
            elif me.is_admin() and role in (Account.EDITOR, 'guest'):
                access = True

            if access:
                return f(self, *args, **kw)
            else:
                return self.render('admin/403.html')
        return _decorator
    return decorator


def handler_security(role='guest'):
    def decorator(f):
        @wraps(f)
        def _decorator(self, *args, **kw):
            f(self, *args, **kw)
            me = self.account
            if me.is_guest() and self.request.path != '/login':
                return self.redirect(self.reverse_url('login'))
            access = False
            if me.is_root():
                access = True
            elif me.inactive():
                access = False
            elif me.role == role:
                access = True
            elif me.is_admin() and role in (Account.EDITOR, 'guest'):
                access = True

            if not access:
                return self.render('admin/403.html')
        return _decorator
    return decorator


class SecurityMeta(type):

    def __new__(metacls, cls_name, bases, attrs):
        role = attrs.get('__role__')

        if role:
            prepare = handler_security(role)(Handler.prepare)
            attrs['prepare'] = prepare
            del attrs['__role__']
        cls = type.__new__(metacls, cls_name, bases, attrs)

        return cls