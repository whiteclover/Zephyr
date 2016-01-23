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


from .field import field_menu


def extend_menu(m):

    with m.menu('/admin') as menu:
        menu.connect("/extend", render="admin/extend/index.html", security='admin')
        menu.connect("/extend/variable", render="admin/extend/variable/index.html", security='admin')
        menu.connect("/extend/variable/add", render="admin/extend/variable/add.html", security='admin')
        menu.connect("/extend/variable/add", render="admin/extend/plugin/index.html", security='admin')

    field_menu(m)
