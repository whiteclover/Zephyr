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

import tornado.web

from .hook import HookMap


class Application(tornado.web.Application):

    hookpoints = ['on_start_request', 'on_end_request',
                'before_error_response', 'after_error_response']

    def __init__(self, handlers, **settings):
        self.error_pages = {}
        self.hooks = HookMap()
        tornado.web.Application.__init__(
            self, handlers, **settings)

    def attach(self, point, callback, failsafe=None, priority=None, **kwargs):
        if point not in self.hookpoints:
            return
        self.hooks.attach(point, callback, failsafe, priority, **kwargs)

    def error_page(self, code, callback):
        if type(code) is not int:
            raise TypeError("code:%d is not int type" % (code))
        self.error_pages[str(code)] = callback
