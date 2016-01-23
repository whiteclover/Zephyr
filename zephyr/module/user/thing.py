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
from .model import User

from zephyr.breeze import Backend
from zephyr.lib.paginator import Paginator
from zephyr.lang import text
from zephyr.lib.validator import EmailValidator
import re

from zephyr.session import Account


email_validator = EmailValidator()


__all__ = ["UserThing"]

class UserThing(object):

    def __init__(self):
        self.repo = Backend(User.__name__)

    get = lambda self, uid: self.repo.find(uid)

    def auth(self, username, password):
        user = self.repo.find_by_username(username)
        if not user:
            return {'status': 404, 'msg': 'not found'}

        if user and not user.inactive() and user.check(password):
            return {'status': 200, 'msg': 'auth success', 'user': user}
        return {'status': 403, 'msg': 'username or password is invaild'}

    def page(self, page, perpage=5):
        total = self.repo.count()
        users = self.repo.take(page, perpage)
        page = Paginator(users, total, page, perpage, '/admin/user')
        return page


    def get_user_page(self, user):
        return Paginator([user], 1, 1, 5, '/admin/user')

    def user_count(self):
        return self.repo.count()

    def check_email(self, email):
        return email_validator(email)

    def add_user(self, username, email, real_name, password, bio, status='', role='user'):
        username, real_name = username.strip(), real_name.strip()
        errors = []
        if not re.match(r'^[A-Za-z0-9_]{4,16}$', username):
            errors.append(text('user.username_missing'))

        if not re.match(r'^[A-Za-z0-9_]{4,16}$', password):
            errors.append(text('user.password_invalid'))

        if not self.check_email(email):
            errors.append(text('user.email_missing'))

        if errors:
            return {'status': 'error', 'errors': errors}

        if status not in Account.STATUSES:
            status = 'inactive'

        if role not in Account.ROLES:
            role = 'user'

        if self.repo.find_by_username(username):
            errors.append(text('user.username_used'))

        if errors:
            return {'status': 'error', 'errors': errors}

        user = User(username, email, real_name, password, None, bio, status, role)
        user.uid = self.repo.create(user)
        return {'status': 'ok', 'msg': 'saved', 'user': user}

    def update_user(self, me, uid, email, real_name, password, newpass1, newpass2, bio, status, role='user'):
        real_name, newpass1, newpass2, bio = real_name.strip(), newpass1.strip(), newpass2.strip(), bio.strip()
        errors = []

        if not self.check_email(email):
            errors.append(text('user.email_missing'))

        if errors:
            return {'status': 'error', 'errors': errors}

        user = self.repo.find(uid)
        if not user:
            return {'status': 'error', 'errors': 'User not Found'}

        if me.uid == user.uid:
            if re.match(r'[A-Za-z0-9@#$%^&+=]{4,16}', newpass1):
                if password and newpass1 and newpass1 == newpass2 and user.check(password):
                    user.secure_pass = newpass1
            elif newpass1:
                errors.append(text('users.password_missing'))

            if self.check_email(email):
                user_ = self.repo.find_by_email(email)
                if user_ and user_.uid != user.uid:
                    errors.append(text('user.email_used'))
                else:
                    user.email = email

        if errors:
            return {'status': 'error', 'errors': errors}

        account = Account.fromUser(user)
        if me.is_root() or me.uid == uid:
            if me.is_root() and not account.is_root():
                if role in (Account.ADMIN, Account.USER, Account.EDITOR):
                    user.role = role
                if user.status != status and status in Account.STATUSES:
                    user.status = status

            if user.real_name != real_name:
                user.real_name = real_name

            if user.bio != bio:
                user.bio = bio

        self.repo.save(user)
        return {'status': 'ok', 'msg': 'updated', 'user': user}


    def delete(self, me, user_id):
        user = self.repo.find(user_id)

        if not user:
            return
        account = Account.fromUser(user)
        if account.is_root():
            return 
        if me.is_root():
            return self.repo.delete(user)