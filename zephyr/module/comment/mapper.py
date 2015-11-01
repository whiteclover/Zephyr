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

from .model import Comment

from zephyr.orm import BaseMapper
import db


__all__ = ['CommentMapper']


class CommentMapper(BaseMapper):

    table = 'comments'
    model = Comment

    def find(self, cid):
        data = db.select(self.table).fields('post_id', 'name',
                                            'email', 'content', 'status', 'created', 'cid').condition('cid', cid).execute()
        if data:
            return self.load(data[0], self.model)

    def find_by_post_id(self, post_id, status='approved'):
        q = db.select(self.table).fields('post_id', 'name',
                                         'email', 'content', 'status', 'created', 'cid').condition('post_id', post_id)
        if status:
            q.condition('status', status)
        data = q.execute()
        return [self.load(_, self.model) for _ in data]

    def paginate(self, page=1, perpage=10, status='all'):
        q = db.select(self.table).fields('post_id', 'name', 'email', 'content', 'status', 'created', 'cid')
        if status != 'all':
            q.condition('status', status)
        results = q.limit(perpage).offset((page - 1) * perpage).order_by('created').execute()
        pages = [self.load(page, self.model) for page in results]
        return pages

    def count(self):
        return db.select(self.table).fields(db.expr('COUNT(*)')).execute()[0][0]

    def spam_count(self, domain):
        return db.select(self.table).fields(db.expr('COUNT(*)')).condition('email', domain, 'LIKE').execute()[0][0]

    def create(self, comment):
        """Create a new comment"""
        return db.execute("INSERT INTO comments(post_id, name, email, content, status, created) VALUES(%s, %s, %s, %s, %s, %s)",
                          (comment.post_id, comment.name, comment.email, comment.content, comment.status, comment.created))

    def save(self, comment):
        """Save Comment"""
        q = db.update(self.table)
        data = dict((_, getattr(comment, _)) for _ in ('post_id', 'name',
                                                       'email', 'content', 'status', 'created', 'cid'))
        q.mset(data)
        return q.condition('cid', comment.cid).execute()

    def delete(self, comment_id):
        """Delete category by commment id"""
        return db.delete(self.table).condition('cid', comment_id).execute()
