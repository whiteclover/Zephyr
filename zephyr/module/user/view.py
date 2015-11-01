#!/usr/bin/env python
#
# Copyright 2015 zephyr
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

def user_menu(m):
    r = m.r

    with m.menu("/admin") as menu:
        menu.connect(r'/login', Login, name="login")
        menu.connect("/logout", Logout, name="logout")
        menu.connect("/user.json", UserJson, name="user_json")
        menu.connect(r('/user/<uid:int>/delete'),DeleteUser, name="user_delete")
        menu.connect('/user', UserPage, name='user_page1')
        menu.connect(r('/user/<page:int>'), UserPage, name='user_page')
        menu.connect(r('/user/<uid:int>/edit'), EditUser, name='user_edit')
        menu.connect('/user/add', AddUser, name="user_add")

from .model import User
from zephyr.breeze import Thing
from zephyr.helper import site as config
from zephyr.lang import text
from zephyr.session import security, ROOT, Account


user_service = Thing('User')

from zephyr.session import SessionManager

class Login:

    def get(self):
        if self.account.is_guest():
            return self.render('admin/user/login.html')
        self.redirect(self.reverse_url('post_page'))

    def post(self):
        _ = self.get_argument
        username, password = _('username'), _('password')

        result = user_service.auth(username, password)
        if result['status'] == 200:
            sessionMgr = SessionManager(self)
            sessionMgr.loadByUser(result['user'])
            return self.redirect(self.reverse_url('post_page'))

        self.flash(text('user.login_error'), 'error')
        return self.redirect(self.reverse_url('login'))


class Logout:

    def get(self):
        sessionMgr = SessionManager(self)
        sessionMgr.logout()
        return self.redirect(self.reverse_url('login'))


class UserJson:

    def get(self):
        return self.jsonify(self.account)


class UserPage:

    @security()
    def get(self, page=1):
        page = int(page)
        me = self.account
        if me.is_root():
            page = user_service.page(page, config.posts_per_page())
        else:
            page = user_service.get_user_page(me)

        self.render('admin/user/index.html', users=page)


class AddUser:

    @security(ROOT)
    def get(self):
        self.render('admin/user/add.html', statuses=Account.STATUSES, roles=Account.ROLES)

    @security(ROOT)
    def post(self):
        p = self.get_argument
        username = p('username')
        email = p('email')
        real_name = p('real_name')
        password = p('password')
        bio = p('bio')
        status = p('status', default='inactive')
        role = p('role', default='user')

        result = user_service.add_user(username, email, real_name, password, bio, status, role)
        if result['status'] == 'ok':
            self.redirect(self.reverse_url('user_edit', uid=result['user'].uid))
        else:
            self.flash(result['errors'], 'error')
            self.render('admin/user/add.html', statuses=Account.STATUSES, roles=Account.ROLES)


class EditUser:

    @security()
    def get(self, uid):
        uid = int(uid)
        if (not (self.account.is_root() or self.account.is_admin())) and self.account.uid != uid:
            return self.render('admin/403.html', message='You can only edit your self')

        user = user_service.get(uid)
        return self.render('admin/user/edit.html', statuses=Account.STATUSES, roles=Account.ROLES, user=user)

    @security()
    def post(self, uid):
        uid = int(uid)
        p = self.get_argument
        email = p('email')
        real_name = p('real_name')
        password = p('password', default='')
        newpass1 = p('newpass1')
        newpass2 = p('newpass2')
        bio = p('bio')
        status = p('status', default='inactive')
        role = p('role', default='user')

        result = user_service.update_user(self.account,
            uid, email, real_name, password, newpass1, newpass2, bio, status, role)
        if result['status'] == 'ok':
            return self.redirect(self.reverse_url('user_edit', result['user'].uid))
        else:
            self.flash(result['errors'], 'error')
            return self.redirect(self.reverse_url('user_edit', uid))


class DeleteUser:

    @security(ROOT)
    def get(uid):
        user_service.delete(self.account, uid)
        self.flash(text('user.deleted'), 'success')
        return self.redirect(self.reverse_url('user_page'))
