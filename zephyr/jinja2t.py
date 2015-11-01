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

from jinja2 import Environment, FileSystemLoader, FileSystemBytecodeCache
from jinja2 import Markup
import jinja2
import tornado.template



class FixedTemplate(jinja2.Template):
    """ Subclass of jinja2.Template
    Override Template.generate method to adapt render_string method\
            from tornado.RequestHandler
    """

    def generate(self, **kwargs):
        return self.render(**kwargs)

# Change The template class that returned by Environment.get_templte
Environment.template_class = FixedTemplate


class Jinja2Loader(tornado.template.Loader):

    """ inherit form tornado.template.Loader
    Implementing customized Template Loader of for tornado to generate\
            jinja2 template
    """

    def __init__(self, root_directory, cache_path=None, cache_size=-1,
                 auto_reload=False,
                 autoescape=True, **kwargs):
        super(Jinja2Loader, self).__init__(root_directory, **kwargs)
        bcc = None
        if cache_path:
            # if not os.path.exists(cache_path):
            #     os.makedirs(cache_path)
            bcc = FileSystemBytecodeCache(directory=cache_path)
        self.env = Environment(loader=FileSystemLoader(self.root), bytecode_cache=bcc,
                               auto_reload=auto_reload,
                               cache_size=cache_size,
                               autoescape=autoescape)

    def _create_template(self, name):
        return self.env.get_template(name)

    def reset(self):
        if hasattr(self.env, 'bytecode_cache') and self.env.bytecode_cache:
            self.env.bytecode_cache.clear()
