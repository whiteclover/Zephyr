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


class PedisBoot(object):

    def __init__(self, options=None):
        self.config(options)

    def config(self, options=None):
        options = options or self.options
        with options.group("Redis settings") as group:
            _ = group.define
            _('--redis.host', default='localhost', help='The host of the redis (default %(default)r)')
            _('--redis.port', default=6379, help='The port of the redis (default %(default)r)', type=int)
            _('--redis.db', default=0, help='The db of the redis (default %(default)r)', type=int)
            _('--redis.password', default=None, help='The user of the redis (default %(default)r)')
            _('--redis.max_connections', default=None, help='The max connections of the redis (default %(default)r)')
