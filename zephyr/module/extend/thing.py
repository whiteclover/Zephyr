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

import os

from .model import Extend, Meta, Field
from zephyr.breeze import Backend
from zephyr.lang import text
from zephyr.lib.image import img_resize
from zephyr.lib.paginator import Paginator
from zephyr.util import secure_filename


__all__ = ['ExtendThing']

class ExtendThing(object):

    def __init__(self):
        self.extend_repo = Backend('Extend')
        self.meta_repo = Backend('Meta')

    def get_by_eid(self, extend_id):
        return self.extend_repo.find(extend_id)

    def field_page(self, page=1, perpage=10, url= '/admin/extend/field'):
        total = self.extend_repo.count()
        pages = self.extend_repo.paginate(page, perpage, url)
        pagination = Paginator(
            pages, total, page, perpage,)
        return pagination

    def get_fields_by_type(self, type='post', node_id=None):
        extends = self.extend_repo.find_by_type(type)
        if node_id is None:
            load_meta = lambda extend: Meta(0, type, extend)
        else:
            load_meta = lambda extend: self.meta_repo.find(
                type, node_id, extend.eid) or Meta(0, type, extend)

        return [Field(extend, load_meta(extend)) for extend in extends]

    def count(self, key, type):
        return self.extend_repo.count(key=key, type=type)

    def create_extend(self, type, key, label, field, attributes):
        extend = Extend(type, key, label, field, attributes)
        self.extend_repo.create(extend)
        return extend

    def update_extend(self, type, key, label, field, attributes, extend_id):
        extend = self.get_by_eid(extend_id)
        if not extend:
            return None
        extend.attributes = attributes
        extend.label = label
        self.extend_repo.save(extend)
        return extend

    def delete_extend(self, extend_id):
        field = self.extend_repo.find(extend_id)
        if not field:
            return None
        return self.extend_repo.delete(field)

    def prcoess_field(self, content_path, node, type='post'):
        FieldMananger(content_path, node, type).process()


class FieldMananger(object):

    def __init__(self, handeler, content_path, node, type='post'):
        self.node = node
        self.content_path = content_path
        self.request = handler.request
        self.handler  = handler
        self.type = type

    def process(self):
        type = self.type
        item_id = self.node.pid
        data = None
        for extend in Backend('Extend').find_by_type(type):
            process = getattr(self, 'process_' + extend.field, None)
            # if process:

            data = process(extend)

            if data:
                meta = Backend('meta').find(type, item_id, extend.eid)
                if meta:
                    meta.data = data
                    Backend('meta').save(meta)
                else:
                    meta = Meta(item_id, type, extend.eid, data)
                    Backend('meta').create(meta)

    def process_image(self, extend):
        uploadFile = request.files['extend_' + extend.key][0]
        filename = secure_filename(uploadFile['filename'])
        if filename:
 
            path = os.path.join(self.content_path, filename)
            name, ext = filename.rsplit('.', 1)
            filename = self.type + '-' + self.node.slug + '.' + ext
            with open(path, 'wb') as fileObj:
                fileObj.write(uploadFile['body'])
            img_resize(path, self.get_size(extend))
            return {'name': filename, 'filename': filename}

    def get_size(self, extend):
        return extend.attributes['size']['width'], extend.attributes['size']['height']

    def process_file(self, extend):
        uploadFile = self.request.files['extend_' + extend.key][0]
        filename = secure_filename(uploadFile['filename'])
        if filename:
            name, ext = filename.rsplit('.', 1)
            filename = self.type + '-' + self.node.slug + '.' + ext
            path = os.path.join(self.content_path, filename)
            with open(path, 'wb') as fileObj:
                fileObj.write(uploadFile['body'])
            return {'name': filename, 'filename': filename}

    def process_text(self, extend):
        text = handler.get_argument('extend_' + extend.key)
        return {'text': text}

    def process_html(self, extend):
        html = request.form.get('extend_' + extend.key)
        return {'html': html}
