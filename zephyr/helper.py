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


from zephyr.lib.memoize import memoize
from zephyr.breeze import Backend


@memoize()
def categories():
    return Backend('Category').categories()


@memoize()
def menus():
    return Backend('Page').menu(True)


@memoize()
def cached_user(uid):
    return Backend('User').find(uid)


class SiteConfig(object):

    def sitename(self):
        return self.config.get('sitename', 'White')

    def description(self):
        return self.config.get('site_description', '')

    def posts_per_page(self, perpage=10):
        return self.config.get('posts_per_page', perpage)

    def comment_moderation_keys(self):
        return self.config.get('comment_moderation_keys', [])

    def get(self, key, default=None):
        return self.config.get(key, default)

    @property
    def config(self):
        return self._config()

    @memoize()
    def _config(self):
        return Backend('Pair').find('system').json_value()

    def clear_cache(self):
        self._config.cache.flush()


site = SiteConfig()
