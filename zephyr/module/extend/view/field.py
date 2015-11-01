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


def field_menu(m):
    r = m.r
    with m.menu('/admin/extend') as menu:
        menu.connect('/field', FieldPage, name='field_page')
        menu.connect(r('/field/<page:int>'), FieldPage, name='field_page')

        menu.connect('/field/add', AddField, name='field_add')
        menu.connect(r('/field/<extend_id:int>/edit'), EditField, name='field_edit')
        menu.connect(r('/field/<extend_id:int>/delete'), DeleteField, name='post_delete')

from zephyr.lib.validator import Validator
from zephyr.helper import site
from zephyr.session import security, ADMIN, EDITOR
from zephyr.breeze import Thing
from zephyr.lang import text

extend_service = Thing('Extend')


class FieldPage:

    @security(ADMIN)
    def get(self,page=1):
        page = int(page)
        extends = extend_service.field_page(page)
        self.render('admin//extend/field/index.html', fields=extends)


class AddField:

    @security(ADMIN)
    def get(self):
        self.render('admin//extend/field/add.html')

    @security(ADMIN)
    def post(self):

        _ = self.get_argument
        _type = _('type')
        field = _('field')
        key = _('key')
        label = _('label')
        key = key or label

        validator = Validator()
        validator.add(
            'valid_key', lambda key: extend_service.count(key, _type) == 0)
        (validator
            .check(key, 'min', text('extend.key_missing'), 1)
            .check(key, 'valid_key', text('extend.key_exists'))
            .check(label, 'min', text('extend.label_missing'), 1)
         )

        if validator.errors:
            self.flash(validator.errors, 'error')
            self.render('admin/extend/field/add.html')

        if field == 'image':
            attributes = {
                'type': reqp.get('attributes[type]'),
                'size': {
                    'height': reqp.get('attributes[size][height]', type=int),
                    'width': reqp.get('attributes[size][width]', type=int),
                }
            }
        elif field == 'file':
            attributes = {
                'type': reqp.get('attributes[type]'),
            }
        else:
            attributes = {}

        extend_service.create_extend(_type, key, label, field, attributes)
        return self.redirect(self.reverse_url('field_page'))


class EditField:
    
    @security(ADMIN)
    def get(self, extend_id):
        extend_id= int(extend_id)
        extend = extend_service.get_by_eid(extend_id)
        self.render('admin//extend/field/edit.html', field=extend)

   
    @security(ADMIN)
    def post(self, extend_id):
        extend_id= int(extend_id)
        reqp = request.form
        _ = self.get_argument
        _type = _('type')
        field = _('field')
        key = _('key')
        label = _('label')
        key = key or label

        validator = Validator()
        (validator
            .check(key, 'min', text('extend.key_missing'), 1)
            .check(label, 'min', text('extend.label_missing'), 1)
         )

        if validator.errors:
            self.flash(validator.errors, 'error')
            return self.redirect(self.reverse_url('field_edit', extend_id))

        if field == 'image':
            attributes = {
                'type': reqp.get('attributes[type]'),
                'size': {
                    'height': reqp.get('attributes[size][height]', type=int),
                    'width': reqp.get('attributes[size][width]', type=int),
                }
            }
        elif field == 'file':
            attributes = {
                'type': reqp.get('attributes[type]'),
            }
        else:
            attributes = {}

        extend_service.update_extend(
            _type, key, label, field, attributes, extend_id)
        return self.redirect(self.reverse_url('field_edit', extend_id))


class DeleteField:

    @security(ADMIN)
    def get(self, extend_id):
        extend_id= int(extend_id)
        extend_service.delete_extend(extend_id)
        return self.redirect(self.reverse_url('field_page'))
