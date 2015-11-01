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


__all__ = ['patch_tornado']

import traceback


def patch_tornado():

    from functools import wraps

    import datetime
    import decimal

    try:
        import simplejson as json  # try external module
    except ImportError:
        import json

    def as_json(o):
        """Returns the json serialize content
        when the o is a object isinstance and has as_json method, then it will call the method, 
        and dumps the return content. Also it can handle the datetime.date and decimal dumps
        """
        if hasattr(o, '__json__') and callable(o.__json__):
            return o.__json__()
        if isinstance(o, (datetime.date,
                          datetime.datetime,
                          datetime.time)):
            return o.isoformat()[:19].replace('T', ' ')
        elif isinstance(o, (int, long)):
            return int(o)
        elif isinstance(o, decimal.Decimal):
            return str(o)
        else:
            raise TypeError(repr(o) + " is not JSON serializable")

    def json_encode(value, ensure_ascii=True, default=as_json):
        """Returns the json serialize stream"""
        return json.dumps(value, default=default, ensure_ascii=ensure_ascii)

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            theme = self.application.config.get('theme', 'default')
            tpl = 'theme/' + theme + '/404.html'
            self.render(tpl, page_title='Not Found')
        else:
            if self.settings.get("serve_traceback") and "exc_info" in kwargs:
                # in debug mode, try to send a traceback
                self.set_header('Content-Type', 'text/plain')
                for line in traceback.format_exception(*kwargs["exc_info"]):
                    self.write(line)
                    self.finish()
            else:
                self.finish("<html><title>%(code)d: %(message)s</title>"
                            "<body>%(code)d: %(message)s</body></html>" % {
                                "code": status_code,
                                "message": self._reason,
                            })

    from tornado import escape
    from tornado import web
    web.RequestHandler.write_error = write_error
    escape.json_encode = json_encode
