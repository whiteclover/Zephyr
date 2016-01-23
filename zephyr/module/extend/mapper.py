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


from zephyr.orm import BaseMapper
import db

from .model import Meta, Extend
from tornado.escape import json_decode, json_encode

__all__ = ['MetaMapper', 'ExtendMapper']


class ExtendMapper(BaseMapper):

    model = Extend
    table = 'extend'

    def find(self, eid):
        """Find and load the extend from database by eid(extend id)"""
        data = (db.select(self.table).fields('type', 'key', 'label', 'field', 'attributes', 'eid').
                condition('eid', eid).execute())
        if data:
            return self.load(data[0])

    def find_by_type(self, type):
        """Find and load the extend from database by eid(extend id)"""
        data = (db.select(self.table).fields('type', 'key', 'label', 'field', 'attributes', 'eid').
                condition('type', type).execute())
        return [self.load(_) for _ in data]

    def paginate(self, page=1, perpage=10):
        data = db.select(self.table).fields('type', 'key', 'label', 'field', 'attributes', 'eid').limit(perpage).offset((page - 1) * perpage).execute()
        return [self.load(_) for _ in data]

    def load(self, data):
        data = list(data)
        try:
            data[4] = loads(data[4])
        except:
            data[4] = dict()
        return BaseMapper.load(self, data, self.model)

    def field(self, type, key, eid=-1):
        field = db.select(self.table).fields('type', 'key', 'label', 'field', 'attributes', 'eid').condition('type', type).condition('key', key).execute()
        if field:
            return self.load(field[0])

    def count(self, **kw):
        q = db.select(self.table).fields(db.expr('COUNT(*)'))
        if kw:
            for k, v in kw.iteritems():
                q.condition(k, v)
        return q.execute()[0][0]

    def create(self, extend):
        """Create a new extend"""
        attributes = dumps(extend.attributes)
        return db.execute('INSERT INTO extend (`type`, `label`, `field`, `key`, `attributes`) VALUES (%s, %s, %s, %s, %s)',
                (extend.type, extend.label, extend.field, extend.key, attributes))

    def save(self, extend):
        """Save and update the extend"""
        attributes = dumps(extend.attributes)
        return (db.update(self.table).
                mset(dict(type=extend.type,
                          label=extend.label,
                          key=extend.key,
                          attributes=attributes,
                          field=extend.field))
                .condition('eid', extend.eid).execute())

    def delete(self, extend):
        """Delete category by extend"""
        return db.delete(self.table).condition('eid', extend.eid).execute()

class MetaMapper(BaseMapper):

    model = Meta
    table = 'meta'

    def find(self, type, node_id, extend_id):
        data = (db.select(self.table).fields('node_id', 'type', 'extend', 'data', 'mid')
                .condition('type', type)
                .condition('node_id', node_id)
                .condition('extend',  extend_id)
                .execute())
        if data:
            return self.load(data[0])

    def load(self, data):
        data = list(data)
        try:
            data[3] = json_decode(data[3])
        except:
            data[3] = dict()
        return BaseMapper.load(self, data, self.model)

    def create(self, meta):
        data = dumps(meta.data)
        return (db.insert(self.table).fields('node_id', 'type', 'extend', 'data')
                .values((meta.node_id, meta.type, meta.extend, data)).execute())

    def save(self, meta):
        data = json_encode(meta.data)
        return (db.update(self.table).mset(
            dict(node_id=meta.node_id,
                 type=meta.type,
                 extend=meta.extend,
                 data=data)).condition('mid', meta.mid).execute())

    def delete(self, meta):
        return db.delete(self.table).codition('mid', meta.mid)
