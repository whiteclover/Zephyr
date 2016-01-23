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


from zephyr.session import SessionManager

def on_load_session(req):
	req.account = None
	SessionManager(req).loadByRequest()


def on_not_found(req, status_code, **kw):
	theme = req.application.config.get('theme', 'default')
	tpl = 'theme/' + theme + '/404.html'
	req.render(tpl, page_title='Not Found')