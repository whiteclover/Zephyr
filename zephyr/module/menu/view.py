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


def menu_menu(m):
    m.connect('/admin/menu', MenuPage, name='menu_page')
    m.connect('/admin/menu/update', UpdateMenu, name='menu_update')


from zephyr.session import security, ADMIN
from zephyr.breeze import Thing

menuservice = Thing('Menu')


class MenuPage:

    @security(ADMIN)
    def get(self):
        pages = menuservice.menu(True)
        self.render('admin/menu/index.html', messages='',
                    pages=pages)


class UpdateMenu:

    @security(ADMIN)
    def post(self):
        sort = self.get_arguments('sort')
        menuservice.update(sort)
        self.jsonify({'return': True})

    get = post
