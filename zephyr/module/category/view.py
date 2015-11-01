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


def category_menu(m):
    r = m.r
    with m.menu("/admin") as menu:
        menu.connect('/category', CategoryPage, name="category_page1")
        menu.connect(r('/category/<page:int>'), CategoryPage, name="category_page")
        menu.connect('/category/add', AddCategory, name="category_add")
        menu.connect(r('/category/<category_id:int>/edit'), EditCategory, name="category_edit")
        menu.connect(r('/category/<category_id:int>/delete'), DeleteCategory, name="category_delete")


from zephyr.breeze import Thing
from zephyr.lang import text
from zephyr.lib.validator import Validator
from zephyr.session import security, ADMIN

category_service = Thing('Category')


class CategoryPage:

    @security(ADMIN)
    def get(self, page=1):
        pagination = category_service.page(page)
        self.render('admin/category/index.html', categories=pagination)


class AddCategory:

    @security(ADMIN)
    def get(self):
        self.render('admin/category/add.html')

    @security(ADMIN)
    def post(self):
        _ = self.get_argument
        title, slug, description = _('title'), _('slug'), _('description')

        validator = Validator()
        validator.check(title, 'min', text('category.title_missing'), 1)
        if validator.errors:
            self.flash(validator.errors, 'error')
            return self.render('admin/category/add.html')

        category_service.add_category(title, slug, description)
        self.redirect(self.reverse_url('category_page'))


class EditCategory:

    @security(ADMIN)
    def get(self, category_id):
        category_id = int(category_id)
        category = category_service.get_by_cid(category_id)
        return self.render('admin/category/edit.html', category=category)

    @security(ADMIN)
    def post(self, category_id):
        _ = self.get_argument
        category_id, title, slug, description = int(category_id), _('title'), _('slug'), _('description')

        validator = Validator()
        validator.check(title, 'min', text('category.title_missing'), 1)
        if validator.errors:
            self.flash(validator.errors, 'error')
            return self.redirect(self.reverse_url('category_edit', category_id))

        category = category_service.update_category(
            category_id, title, slug, description)
        self.flash(text('category.updated'), 'success')
        self.redirect(self.reverse_url('category_edit', category.cid))


class DeleteCategory:

    @security(ADMIN)
    def post(self, category_id):
        category_id = int(category_id)
        if category_id == 1:
            self.flash('The Uncategory cann\'t delete', 'error')
            return self.redirect(self.reverse_url('category_page'))

        category_service.delete(category_id)
        self.flash(text('category.deleted'), 'success')
        self.redirect(self.reverse_url('category_page'))

    get = post
