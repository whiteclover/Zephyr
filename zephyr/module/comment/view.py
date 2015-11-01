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



def comment_menu(m):
    r = m.r
    with m.menu("/admin") as menu:
        menu.connect('/comment', CommentPage, name="comment_page1")
        menu.connect(r('/comment/<status>'), CommentPage, name="comment_page2")
        menu.connect(r('/comment/<status>/<page:int>'), CommentPage, name="comment_page3")
        menu.connect(r('/comment/<comment_id:int>/edit'), EditComment, name="comment_edit")
        menu.connect(r('/comment/<comment_id:int>/delete'), DeleteComment, name="comment_delete")


from zephyr.session import security, ADMIN, EDITOR
from zephyr.breeze import Thing
from zephyr.lang import text
from zephyr.lib.validator import Validator

from zephyr.helper import site


comment_service = Thing('Comment')

COMMENT_STATUSES = [
    {'url': 'all', 'lang': text('global.all'), 'class': 'all'},
    {'url': 'pending', 'lang': text('global.pending'), 'class': 'pending'},
    {'url': 'approved', 'lang': text('global.approved'), 'class': 'approved'},
    {'url': 'spam', 'lang': text('global.spam'), 'class': 'spam'}
]


class CommentPage:

    @security(EDITOR)
    def get(self, page=1, status='all'):
        page = int(page)
        pagination = comment_service.page(status, page, site.posts_per_page())
        self.render('admin//comment/index.html',
                               statuses=COMMENT_STATUSES,
                               status=status,
                               comments=pagination)


class EditComment:

    @security(EDITOR)
    def get(self, comment_id):
        comment_id = int(comment_id)
        
        statuses = {
                'approved': text('global.approved'),
                'pending': text('global.pending'),
                'spam': text('global.spam')
            }
        comment = comment_service.get(comment_id)
        
        self.render('admin/comment/edit.html',
                               comment=comment,
                                   statuses=statuses)
    @security(EDITOR)
    def post(self, comment_id):
        comment_id = int(comment_id)
        _ = self.get_argument
        name = _('name')
        email = _('email')
        content = _('content')
        status = _('status')

        name, content = name.strip(), content.strip()

        validator = Validator()
        (validator.check(name, 'min', text('comment.name_missing'), 1)
            .check(content, 'min', text('comment.content_missing'), 1)
         )
        if validator.errors:
            self.flash(validator.errors, 'error')
            self.redirect(self.reverse_url('comment_edit', comment_id=comment_id))

        comment = comment_service.update_comment(
            comment_id, name, email, content, status)
        self.flash(text('comment.updated'), 'success')
        self.redirect(self.reverse_url('comment_edit', comment.cid))


class DeleteComment:
    @security(EDITOR)
    def get(self, comment_id):
        comment_id = int(comment_id)
        comment_service.delete(comment_id)
        self.flash(text('comment.deleted'), 'success')
        self.redirect(self.reverse_url('comment_page'))

    post = get
