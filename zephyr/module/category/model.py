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

from zephyr.breeze import Backend

__all__ = ['Category']


class Category(object):

    def __init__(self, title, slug, description, cid=None):
        """The Category is used by post and page model. when load from database it takes the cid"""
        self.title = title
        self.slug = slug
        self.description = description
        if cid is not None:
            self.cid = cid

    def __str__(self):
        return '<Category cid: %d, title: %s, slug: %s>' % (self.cid, self.title, self.slug)

    def is_uncategory(self):
        return self.cid == 1

    def category_url(self):
        return '/category/' + self.slug

    def category_count(self):
        return Backend('Post').category_count(self.cid)
