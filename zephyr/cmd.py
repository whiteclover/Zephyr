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
import sys

from zephyr import options
from zephyr.boot import BootOptions
from zephyr.config import SelectConfig, ConfigFactory


class Null(object):
    pass

_Null = Null()


class Cmd(object):

    def __init__(self, opt=None):

        self.options = opt or options

    def get_file_opt(self):
        opt = options.Options(None)
        opt.define('-c', '--config', default='/etc/zephyr/app.conf',
                   help="config path (default %(default)r)", metavar="FILE")
        o = opt.parse_args(sys.argv)
        if os.path.exists(o.config):
            config = ConfigFactory.parseFile(o.config, pystyle=True)
            return config
        else:
            return {}

    def parse_cmd(self, help_doc):
        self.options.setup_options(help_doc)
        BootOptions(self.options)

        self._set_defaults()
        opt = self.options.parse_args()
        config = SelectConfig()
        config.update(vars(opt))
        return config

    def _set_defaults(self):
        c = self.get_file_opt()
        opt = options.Options(None)
        BootOptions(opt)
        opt = opt.parse_args()
        d = {}
        config = vars(opt)
        for k in config:
            v = c.get(k, _Null)
            if v != _Null:
                d[k] = v
        self.options.set_defaults(**d)


__cmd = Cmd()


def parse_cmd(help_doc):
    return __cmd.parse_cmd(help_doc)
