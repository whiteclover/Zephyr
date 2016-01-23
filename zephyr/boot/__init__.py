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

import os


class BootOptions(object):

    def __init__(self, options):
        self.options = options
        self.mod_prefix = 'zephyr.boot.'
        self.auto_boot()

    def auto_boot(self):
        current_path = os.path.dirname(__file__)
        for name in os.listdir(current_path):
            path = os.path.join(current_path, name)
            prefix, ext = name.split(".")
            if ext == 'py' and prefix != '__init__':
                boot_path = self.mod_prefix + prefix + '.' + prefix.capitalize() + 'Boot'
            else:
                continue
            boot = self._import_boot(boot_path)
            if boot:
                boot(self.options)

    def _import_boot(self, module2object):
        try:
            d = module2object.rfind(".")
            menu_func = module2object[d + 1: len(module2object)]
            m = __import__(module2object[0:d], globals(), locals(), [menu_func])
            return getattr(m, menu_func, None)
        except ImportError:
            return None


class Bootable(object):

    def startup(self):
        raise NotImplementedError("Must implement startup in subclass")

    def suhtdown(self):
        raise NotImplementedError("Must implement shutdown in subclass")
