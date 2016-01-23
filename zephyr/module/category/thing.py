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

from zephyr.breeze import Backend

from .model import Category


from zephyr.lib.paginator import Paginator
from zephyr.lang import text

__all__ = ['CategoryThing']

class CategoryThing(object):

    def __init__(self):
        self.category_repo = Backend(Category.__name__)
        self.post_repo = Backend('Post')

    def get_by_cid(self, category_id):
        return self.category_repo.find(category_id)

    def dropdown(self):
        return self.category_repo.dropdown()

    def page(self, page=1, perpage=10):
        total = self.category_repo.count()
        pages = self.category_repo.paginate(page, perpage)
        pagination = Paginator(pages, total, page, perpage, '/admin/category')
        return pagination

    def add_category(self, title, slug, description):
        category = Category(title, slug, description)
        cid = self.category_repo.create(category)
        category.cid = cid
        return category

    def update_category(self, category_id, title, slug, description):
        slug = slug or title
        category = Category(title, slug, description, category_id)
        self.category_repo.save(category)
        return category

    def delete(self, category_id):
        if category_id == 1:
            return
        category = self.category_repo.find(category_id)
        if category and self.category_repo.delete(category_id):
            self.post_repo.reset_post_category(category_id)
