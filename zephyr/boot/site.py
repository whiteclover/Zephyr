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


class SiteBoot(object):

    def __init__(self, options=None):
        self.config(options)

    def config(self, options=None):
        from zephyr import __version__
        options = options or self.options
        group = options.group("Service settings")
        _ = group.define
        _('-H',  '--tornado.host', default='localhost', help='The host of the tornado server (default %(default)r)')
        _('-p', '--tornado.port', default=8888, help='The port of the tornado  server (default %(default)r)', type=int)
        _('-d', '--debug',  help='Open debug mode (default %(default)r)', action='store_true', default=False)
        _('--language', default='en_GB',  help="The language for the site (default %(default)r)")
        _('--content_path', default='/upload',  help="The Upload path for storing uploaded assets (default %(default)r)")
        _('--theme', default='default',  help="The theme for the site (default %(default)r)")
        _('--secert_key', default="7oGwHH8NQDKn9hL12Gak9G/MEjZZYk4PsAxqKU4cJoY=", help='The secert key for secure cookies (default %(default)r)')
        _('-c', '--config', default='/etc/zephyr/app.conf',  help="config path (default %(default)r)", metavar="FILE")
        _("-v", "--version", help="Show zephyr version %s" % __version__)
