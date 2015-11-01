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


from zephyr.orm import BaseMapper
import db



__all__ = ['CategoryMapper']

from .model import Category

class CategoryMapper(BaseMapper):

    table = 'categories'
    model = Category

    def find(self, cid):
        """Find category by category id, return the category model instance if category id exists in database"""
        data = db.select(self.table).fields('title', 'slug', 'description', 'cid').condition('cid', cid).execute()
        if data:
            return self.load(data[0], self.model)

    def dropdown(self):
        """Returns the all category id"""
        return db.select(self.table).fields('cid', 'title').execute(as_dict=True)

    def order_by_title(self):
        results = db.select(self.table).fields('title', 'slug', 'description', 'cid').order_by('title').execute()
        return [self.load(data, self.model) for data in results]

    categories = order_by_title

    def find_by_slug(self, slug):
        """Find all categories by slug  sql like rule"""
        data = db.select(self.table).fields('title', 'slug', 'description', 'cid').condition('slug', slug).execute()
        if data:
            return self.load(data[0], self.model)

    def count(self):
        return db.select(self.table).fields(db.expr('COUNT(*)')).execute()[0][0]

    def paginate(self, page=1, perpage=10):
        """Paginate the categories"""
        results = (db.select(self.table).fields('title', 'slug', 'description', 'cid')
                   .limit(perpage).offset((page - 1) * perpage)
                   .order_by('title').execute())
        return [self.load(data, self.model) for data in results]

    def create(self, category):
        """Create a new category"""
        return db.execute("INSERT INTO categories(title, slug, description) VALUES(%s, %s, %s)",
                          (category.title, category.slug, category.description))

    def save(self, category):
        """Save and update the category"""
        return (db.update(self.table).
                mset(dict(title=category.title,
                          description=category.description,
                          slug=category.slug))
                .condition('cid', category.cid).execute())

    def delete(self, category_id):
        """Delete category by category id"""
        return db.delete(self.table).condition('cid', category_id).execute()
