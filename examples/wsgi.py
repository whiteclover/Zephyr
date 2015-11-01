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

import tornado.wsgi

from cherrypy.wsgiserver import CherryPyWSGIServer

from zephyr.app import ZephyrApp
from zephyr.config import ConfigFactory

if __name__ == "__main__":
    config = ConfigFactory.parseFile('$your_conf', pystyle=True)  # or use SelectConfig
    app = ZephyrApp(config)
    wsgi_app = tornado.wsgi.WSGIAdapter(app)
    server = CherryPyWSGIServer(
        (config.get('cherry.host', 'localhost'), config.get('cherry.port', 8888)),
        wsgi_app,
        server_name='Zephyr',
        numthreads=30)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
