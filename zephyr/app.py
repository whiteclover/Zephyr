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
import os.path


import db
from zephyr import pedis
from zephyr.autoload import AutoLoader
from zephyr.jinja2t import Jinja2Loader
import zephyr.breeze

import zephyr.hooks

class ZephyrApp(zephyr.breeze.Application):

    def __init__(self, config):
        self.config = config
        template_loader = self.boot_template()
        self.boot_database()
        
        self.autoload = AutoLoader()
        self.autoload.autoload()

        settings = dict(
            static_path=config.get("asset.path", os.path.join(os.path.dirname(__file__), "asset")),
            static_url_prefix=config.get("asset.url_prefix", "/assets/"),
            template_loader=template_loader,
            debug=self.config.get("debug", False),
            cookie_secret=self.config.get("secert_key", None)
        )
        zephyr.breeze.Application.__init__(
            self, self.autoload.routes, **settings)

        self.hooks.attach("on_start_request", zephyr.hooks.on_load_session)
        self.error_page(404, zephyr.hooks.on_not_found)

    def boot_template(self):
        template_loader = Jinja2Loader(
            os.path.join(os.path.dirname(__file__), "template"),
            self.config.get("jinja2.cache_path"),
            self.config.get("jinja2.cache_size", -1),
            auto_reload=self.config.get("jinja2.auto_reload", False))

        from zephyr import lang
        from zephyr.lang import text
        from zephyr.helper import categories, menus, site
        from zephyr.util import markdown

        lang.setup(self.config.get('language', 'en_GB'))

        template_loader.env.globals.update(__=text)
        template_loader.env.globals.update(site_categories=categories, menus=menus)
        template_loader.env.globals.update(site=site, enumerate=enumerate)

        template_loader.env.filters['markdown'] = markdown
        return template_loader

    def boot_database(self):
        db.setup(self.config.get('db'))
        pedis.setup(**self.config.get('redis'))


import logging 
import tornado.ioloop
from zephyr import cmd
from zephyr.boot import Bootable
from zephyr.log import log_config

LOG = logging.getLogger('app')

class ZephyrService(Bootable):

    def __init__(self):
        self.config = cmd.parse_cmd("zephyrd")
        log_config("zephyr", self.config.get("debug", False))
        self.application = ZephyrApp(self.config)

    def startup(self):
        try:
            port = self.config.get("tornado.port", 8888)
            host = self.config.get("tornado.host", 'localhost')
            LOG.info("Starting zephyr on %s:%s", host, port)
            self.application.listen(port, host)
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt as e:
            self.shutdown()

    def shutdown(self):
        tornado.ioloop.IOLoop.instance().stop()
