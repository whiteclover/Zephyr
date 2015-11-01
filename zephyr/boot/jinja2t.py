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


class Jinja2tBoot(object):

    def __init__(self, options=None):
        self.config(options)

    def config(self, options=None):
        options = options or self.options
        group = options.group("Jinja2 settings")
        _ = group.define
        _('--jinja2.cache_path', default=None, help='Jinja2 cache code byte path: (default %(default)r)')
        _('--jinja2.cache_size', default=-1, type=int, help='Jinja2 cache size: (default %(default)r)')
        _('--jinja2.auto_reload', action='store_true', default=False, help='Jinja2 filesystem checks (default %(default)r)')
