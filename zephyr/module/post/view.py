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

def post_menu(m):
    r = m.r
    with m.menu('/admin') as menu:
        menu.connect('/post', PostPage, name='post_page')
        menu.connect(r('/post/<page:int>'), PostPage, name='post_page1')
        menu.connect(r('/post/category/<category:int>'), PostPage, name='post_page3')
        menu.connect(r('/post/category/<category:int>/<page:int>'), PostPage, name='post_page4')
        menu.connect('/post/add', AddPost, name='post_add')
        menu.connect(r('/post/<post_id:int>/edit'), EditPost, name='post_edit')
        menu.connect(r('/post/<post_id:int>/delete'), DeletePost, name='post_delete')


from .model import Post
from zephyr.lib.validator import Validator
from zephyr.helper import site


from zephyr.session import security, ADMIN, EDITOR
from zephyr.breeze import Thing, Backend
from zephyr.lang import text


post_service = Thing('Post')
category_service = Thing('Category')
extend_service = Thing('Extend')

STATUSES = {
    'published': text('global.published'),
    'draft': text('global.draft'),
    'archived': text('global.archived'),
}


class PostPage:

    @security(EDITOR)
    def get(self, page=1, category=None):
        page = int(page)
        if category is not None:
            category = int(category)
        pagination = post_service.page(page, site.posts_per_page(), category)
        self.render('admin//post/index.html',
	                           categories=category_service.dropdown(),
	                           posts=pagination,
	                           category=category)


class AddPost:

    @security(EDITOR)
    def get(self):
        fields = extend_service.get_fields_by_type('post')
        self.render('admin/post/add.html', statuses=STATUSES,
            categories=category_service.dropdown(),
	       fields=fields)

    @security(EDITOR)
    def post(self):
        _ = self.get_argument
        title = _('title', default='')
        description = _('description')
        category = int(_('category', default=1))
        status = _('status', default='draft')
        comments = int(_('comments', default=0))
        html = _('html')
        css = _('custom_css', default='')
        js = _('custom_js', default='')
        slug = _('slug')

        title = title.strip()
        slug = slug.strip() or title

        validator = Validator()
        (validator.check(title, 'min', text('post.title_missing'), 1)
	        .check(slug, 'min', text('post.title_missing'), 1)
	     )
        if validator.errors:
            self.flash(validator.errors, 'error')
            self.render('admin/post/add.html')

        author = self.account
        post = post_service.add_post(
            title, slug, description, html, css, js, category, status, comments, author)
        extend_service.prcoess_field(self, post, 'post')
        self.redirect(self.reverse_url('post_page'))


class EditPost:


    @security(EDITOR)
    def get(self, post_id):
        post_id = int(post_id)
        fields = extend_service.get_fields_by_type('post', post_id)
        self.render('admin/post/edit.html',
                                   statuses=STATUSES,
                                   categories=category_service.dropdown(),
                                   article=post_service.get_by_pid(post_id),
                                   fields=fields)


    @security(EDITOR)
    def post(self, post_id):
        post_id = int(post_id)
        _ = self.get_argument
        title = _p('title', default='')
        description = _p('description')
        category = int(_p('category', default=1))
        status = _p('status', default='draft')
        comments = int(_p('comments', default=0))
        html = _p('html')
        css = _p('custom_css', default='')
        js = _p('custom_js', default='')
        slug = _p('slug')

        title = title.strip()
        slug = slug.strip() or title

        validator = Validator()
        (validator.check(title, 'min', text('post.title_missing'), 1)
         .check(slug, 'min', text('post.title_missing'), 1))
        if validator.errors:
            self.flash(validator.errors, 'error')
            self.redirect(self.reverse_url('post_edit', post_id))

        post = post_service.update_post(
            title, slug, description, html, css, js, category, status, comments, post_id)
        extend_service.prcoess_field(self, post, 'post')
        self.flash(text('post.updated'), 'success')
        self.redirect(self.reverse_url('post_edit', post_id))


class DeletePost:

    @security(EDITOR)
    def get(self, post_id):
        post_id = int(post_id)
        post_service.delete(post_id)
        self.flash(text('post.deleted'), 'success')
        self.redirect(self.reverse_url('post_page'))
