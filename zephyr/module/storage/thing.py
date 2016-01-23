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


import re

from .mapper import PairMapper
from .model import Pair
from tornado.escape import json_encode



__all__ = ['PairThing']


class PairThing(object):

    def __init__(self):
        self.pair_repo = PairMapper()

    def site_meta(self):
        return self.pair_repo.find('system')

    def update_site_meta(self, sitename, description, site_page,
                         posts_per_page, auto_published_comments,  comment_moderation_keys):

        meta = self.site_meta()
        config = meta.json_value()

        try:
            sitename = sitename or sitename.strip()
            if sitename:
                config['sitename'] = sitename

            description = description or description.strip()
            if description:
                config['description'] = description

            site_page = int(site_page)
            if site_page >= 0:
                config['site_page'] = site_page

            posts_per_page = int(posts_per_page)
            if posts_per_page:
                config['posts_per_page'] = posts_per_page

            auto_published_comments = bool(auto_published_comments)
            config['auto_published_comments'] = auto_published_comments
            if comment_moderation_keys is not None:
                keys = [key.strip() for key in re.split(' +', comment_moderation_keys) if key.strip()]
                config['comment_moderation_keys'] = keys
            meta.value = json_encode(config)
            self.pair_repo.update(meta)
            return True
        except:
            return False
