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


def page_menu(m):
    r = m.r
    with m.menu('/admin') as menu:
        menu.connect('/page', PagePage, name='page_page')
        menu.connect(r('/page/<page:int>'), PagePage, name='page_page2')
        menu.connect(r('/page/status/<status>'), PagePage, name='page_page3')
        menu.connect(r('/page/status/<status>/<page:int>'), PagePage, name='page_page4')
        menu.connect('/page/add', AddPage, name='page_add')
        menu.connect(r('/page/<page_id:int>/edit'), EditPage, name='page_edit')
        menu.connect(r('/page/<page_id:int>/delete'), DeletePage, name='page_delete')

from .model import Page
from zephyr.lib.validator import Validator
from zephyr.helper import site


from zephyr.session import security, ADMIN, EDITOR
from zephyr.breeze import Thing, Backend
from zephyr.lang import text


PAGE_STATUSES = {
    'published': text('global.published'),
    'draft': text('global.draft'),
    'archived': text('global.archived'),
}

page_service,  extend_service= Thing('Page'), Thing('Extend')



class PagePage:


    @security(EDITOR)
    def get(self, page=1, status='all'):
        pagination = page_service.page(status, page, site.posts_per_page())
        self.render('admin/page/index.html',
                               status=status,
                               pages=pagination)


class EditPage:

    @security(EDITOR)
    def get(self, page_id):
        page_id = int(page_id)
        pages = Backend('Page').dropdown(show_empty_option=True)
        page = Backend('Page').find(page_id)
        fields = extend_service.get_fields_by_type('page', page_id)
        self.render('admin/page/edit.html',
                                   statuses=PAGE_STATUSES,
                                   pages=pages,
                                   page=page,
                                   fields=fields)

    @security(EDITOR)
    def post(self, page_id):
        page_id = int(page_id)

        _ = self.get_argument
        parent = _('parent')
        name = _('name')
        title = _('title')
        name = name or title

        slug = _('slug')
        content = _('content')
        status = _('status')
        show_in_menu = int(_('show_in_menu', default=0))
        show_in_menu = 1 if show_in_menu else 0

        redirect_ = _('redirect')

        validator = Validator()
        (validator
            .check(title, 'min', text('page.title_missing'), 3)
            #.check(redirect, 'url', text('page.redirect_missing'))
         )

        if validator.errors:
            self.flash(validator.errors, 'error')
            self.redirect(self.reverse_url('page_edit', page_id))

        page = page_service.update_page(
            parent, name, title, slug, content, status, redirect_, show_in_menu, page_id)
        extend_service.prcoess_field(self, page, 'page')
        self.redirect(self.reverse_url('page_edit', page_id))



class AddPage:

    @security(EDITOR)
    def get(self):
        if request.method == 'GET':
            pages = Backend('Page').dropdown(show_empty_option=True)
            fields = extend_service.get_fields_by_type('page')
            self.render('admin/page/add.html',
                                   statuses=PAGE_STATUSES,
                                   pages=pages,
                                   fields=fields)


    @security(EDITOR)
    def post(self):
        _ = self.get_argument
        parent = _('parent')
        name = _('name')
        title = _('title')
        name = name or title

        slug = _('slug')
        content = _('content')
        status = _('status')
        pid = int(_('pid'))
        show_in_menu = int(_('show_in_menu'))
        show_in_menu = 1 if show_in_menu else 0

        redirect_ = _('redirect')

        validator = Validator()
        validator.add(
            'duplicate', lambda key: page_service.is_exist_slug(key) == False)
        (validator
            .check(title, 'min', text('page.title_missing'), 3)
            .check(slug, 'min', text('page.slug_missing'), 3)
            .check(slug, 'duplicate', text('page.slug_duplicate'))
            .check(slug, 'regex', text('page.slug_invalid'), r'^[0-9_A-Za-z-]+$')
            #.check(redirect, 'url', text('page.redirect_missing'))
         )

        if validator.errors:
            self.flash(validator.errors, 'error')
            pages = Backend('Page').dropdown(show_empty_option=True)
            fields = extend_service.get_fields_by_type('page')
            self.render('admin/page/add.html',
                                   statuses=PAGE_STATUSES,
                                   pages=pages,
                                   fields=fields)

        page = page_service.add_page(
            parent, name, title, slug, content, status, redirect_, show_in_menu)
        extend_service.prcoess_field(self, page, 'page')
        self.redirect(self.reverse_url('page_page'))


class DeletePage:

    @security(EDITOR)
    def get(slef, page_id):
        page_id = int(page_id)
        page_service.delete(page_id)
        self.redirect(self.reverse_url('page_page'))
