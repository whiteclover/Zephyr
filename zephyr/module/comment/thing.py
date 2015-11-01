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

import re

from zephyr.breeze import Backend
from .model import Comment
from zephyr.lib.paginator import Paginator
from zephyr.lang import text
from zephyr.helper import site


__all__ = ['CommentThing']


class CommentThing(object):

    comment_repo = Backend('Comment')

    get = lambda self, cid: self.comment_repo.find(cid)

    def get_by_post_id(self, post_id):
        return self.comment_repo.find_by_post_id(post_id)

    def page(self, status, page=1, perpage=10):
        total = self.comment_repo.count()
        pages = self.comment_repo.paginate(page, perpage, status)
        pagination = Paginator(pages, total, page, perpage, '/admin/comment')
        return pagination

    def add_comment(self, name, email, content, status, post):
        comment = Comment(post.pid, name, email, content, status)
        if self.is_spam(comment):
            comment.status = 'spam'
        cid = self.comment_repo.create(comment)
        comment.cid = cid
        return comment

    @classmethod
    def is_spam(self, comment):
        for word in site.comment_moderation_keys():
            if word.strip() and re.match(word, comment.content, re.I):
                return True

        domain = comment.email.split('@')[1]
        if self.comment_repo.spam_count(domain):
            return True
        return False

    def update_comment(self, comment_id, name, email, content, status):
        comment = self.get(comment_id)
        if not comment:
            return None
        comment.status = status
        comment.name = name
        comment.content = content
        comment.email = email
        self.comment_repo.save(comment)
        return comment

    def delete(self, comment_id):
        comment = self.comment_repo.find(comment_id)
        if not comment:
            return None
        return self.comment_repo.delete(comment.cid)
