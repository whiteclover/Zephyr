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

import logging 
import os
import os.path
import re

from zephyr import breeze
from zephyr.breeze import Handler, RenderHandler, url
from zephyr.session import SecurityMeta
from zephyr.util import with_metaclass


LOG = logging.getLogger('autoload')

class AutoLoader(object):
    
    REG = re.compile(r"(\w[\w\d_]+)\s*\-\s*>\s*(\w[\w\d_]+)")

    def __init__(self, mod_prefix=None):
        self.routes = []
        self.models = {}
        self.mappers = {}
        self.things = {}
        self.mod_prefix = mod_prefix or 'zephyr.module.'
        self.urltool = URLTool()

    def autoload(self):
        self.mount_model()
        self.mount_mapper()
        self.mount_thing()
        self.mount_menu()

    def mount_model(self):
        current_path = os.path.dirname(__file__)
        module_path = os.path.join(current_path, 'module')
        for name in os.listdir(module_path):
            path = os.path.join(module_path, name)
            if os.path.isdir(path):
                try:
                    model_path = self.mod_prefix + name + '.model'
                    m = __import__(model_path, globals(), locals(), ['__all__'])
                    names = getattr(m,  '__all__', [])
                    for model_name in names:
                        model = getattr(m,  model_name, None)
                        if model:
                            self.models[model_name] = model
                except ImportError as e:
                    LOG.warning("In module %s : %s", model_path, e)
                    continue
        setattr(breeze.core, '__model', self.models)

    def mount_mapper(self):
        current_path = os.path.dirname(__file__)
        module_path = os.path.join(current_path, 'module')
        for name in os.listdir(module_path):
            path = os.path.join(module_path, name)
            if os.path.isdir(path):
                try:
                    model_path = self.mod_prefix + name + '.mapper'
                    m = __import__(model_path, globals(), locals(), ['__all__'])
                    names = getattr(m,  '__all__', [])

                    for mapper_name in names:
                        mapper = getattr(m,  mapper_name, None)
                        if mapper:
                            self.mappers[mapper_name[:-6]] = mapper()
                except ImportError as e:
                    continue

        setattr(breeze.core, '__backend', self.mappers)

    def mount_thing(self):
        current_path = os.path.dirname(__file__)
        module_path = os.path.join(current_path, 'module')
        for name in os.listdir(module_path):
            path = os.path.join(module_path, name)
            if os.path.isdir(path):
                try:
                    model_path = self.mod_prefix + name + '.thing'
                    m = __import__(model_path, globals(), locals(), ['__all__'])
                    names = getattr(m,  '__all__', [])
                    for thing_name in names:
                        thing = getattr(m,  thing_name, None)
                        if thing:
                            self.things[thing_name[:-5]] = thing()
                except ImportError as e:
                    continue

        setattr(breeze.core, '__thing', self.things)

    def mount_menu(self):
        current_path = os.path.dirname(__file__)

        module_path = os.path.join(current_path, 'module')
        for name in os.listdir(module_path):
            path = os.path.join(module_path, name)

            if os.path.isdir(path):
                menu_path = self.mod_prefix + name + '.view.' + name + '_menu'

            else:
                prefix, ext = name.split(".")
                if ext == 'py' and prefix != '__init__':
                    menu_path = self.mod_prefix + prefix + '.' + prefix + '_menu'
                else:
                    continue
            menu = self._import_menu(menu_path)
            if menu:
                menu(self)

    def menu(self, prefix_path):
        return Menu(prefix_path, self)

    def r(self, url):
        return self.urltool.url(url)

    def connect(self, url_spec, handler=None, settings=None, name=None, render=None, security=None):
        if render:
            handler = RenderHandler
            if security:
                class SecurityRenderHandler(with_metaclass(SecurityMeta, (RenderHandler,))):
                    __role__ = security
                handler = SecurityRenderHandler
            self.routes.append((url_spec, handler, dict(template=render)))
            return

        if handler is None:
            raise ValueError("Handler is required, can't be empty")

        self.load_mapper(handler)
        self.load_thing(handler)

        if not issubclass(handler, Handler):
            classes = [Handler] + list(handler.__bases__)
            attrs = dict(handler.__dict__)
            if security:
                attrs['prepare'] = handler_security(security)(Handler.prepare)
            handler = type(handler.__name__, tuple(classes), dict(handler.__dict__))

        self.routes.append(url(url_spec, handler, settings, name))


    def load_mapper(self, handler):

        doc = getattr(handler,  '__mapper__', "")
        if doc:
            lines = [part.strip() for part in doc.split("\n") if part.strip()]
            for line in lines:
                match = self.REG.match(line)
                if match:
                    name, model_name = match.group(1), match.group(2)
                    setattr(handler, name, self.mappers[model_name])

            delattr(handler, '__mapper__')

    def load_thing(self, handler):

        doc = getattr(handler,  '__thing__', "")
        if doc:
            lines = [part.strip() for part in doc.split("\n") if part.strip()]
            for line in lines:
                match = self.REG.match(line)
                if match:
                    name, model_name = match.group(1), match.group(2)
                    setattr(handler, name, self.things[model_name])

            delattr(handler, '__thing__')

    def _import_menu(self, module2object):
        try:
            d = module2object.rfind(".")
            menu_func = module2object[d + 1: len(module2object)]
            m = __import__(module2object[0:d], globals(), locals(), [menu_func])
            return getattr(m, menu_func, None)
        except ImportError:
            return None


class Menu(object):

    def __init__(self, prefix_path, autoload):
        self.prefix_path = prefix_path
        self.autoload = autoload

    def __enter__(self):
        return self

    def connect(self,  url_spec, *args, **kw):
        self.autoload.connect(self.prefix_path + url_spec, *args, **kw)

    def r(self, url):
        return self.autoload.r(url)

    def __exit__(self, exc_type, exc_value, traceback):
        pass


class URLTool(object):
    RULE_RE = re.compile(
        r"""<([a-zA-Z_][a-zA-Z0-9_]*)(?::([a-zA-Z_][a-zA-Z0-9_]*|\(.*\)))?>""")
    DEFAULT_PATTERNS = {
        'int': r'-?\d+',
        'any': r'[^/]+',
        'float': r'-?\d+\.\d+',
    }

    def __init__(self):
        self.patterns = self.DEFAULT_PATTERNS.copy()

    def add_pattern(self, name, pattern):
        self.patterns[name] = pattern

    def url(self, rule):
        end = 0
        ms = self.RULE_RE.finditer(rule)
        pattern = ''
        regex = False
        if ms:
            for m in ms:
                regex = True
                label, p = m.group(1),  m.group(2) or 'any'
                pp = self.patterns.get(p)
                pattern += rule[end:m.start()]
                if pp:
                    pattern += '(?P<%s>%s)' % (label, pp)
                else:
                    pattern += '(?P<%s>%s)' % (label, p[1:-1])
                end = m.end()

        if regex:
            pattern += rule[end:]
            pattern = '%s' % pattern

        return pattern
