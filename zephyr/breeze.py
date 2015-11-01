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

from tornado.escape import utf8, json_encode, json_decode
from tornado.web import RequestHandler, url, StaticFileHandler


__all__ = ['Handler',
           'RenderHandler',
           'Backend', 'Model', 'Thing',
           'url'
           ]


def Backend(key):
    return __backend.get(key)


def Thing(key):
    return __thing.get(key)


def Model(key):
    return __model.get(key)


from zephyr.session import SessionManager, handler_security
from zephyr.flash import FlashMessagesMixin


class Handler(RequestHandler, FlashMessagesMixin):

    def prepare(self):
        self.account = None
        SessionManager(self).loadByRequest()

    @property
    def remote_ip(self):
        return self.request.remote_ip

    def get_current_user(self):
        """Override to determine the current user from, e.g., a cookie."""
        return self.account

    @property
    def current_user(self):
        """The authenticated user for this request.

        This is a cached version of `get_current_user`, which you can
        override to set the user based on, e.g., a cookie. If that
        method is not overridden, this method always returns None.

        We lazy-load the current user the first time this method is called
        and cache the result after that.
        """
        if not hasattr(self, "account"):
            self.account = self.get_current_user()
        return self.account

    @current_user.setter
    def current_user(self, value):
        self.account = value

    def get_template_namespace(self):
        """Returns a dictionary to be used as the default template namespace.

        May be overridden by subclasses to add or modify values.

        The results of this method will be combined with additional
        defaults in the `tornado.template` module and keyword arguments
        to `render` or `render_string`.
        """
        namespace = dict(
            handler=self,
            flash=self.get_flashed_messages,
            request=self.request,
            current_user=self.current_user,
            locale=self.locale,
            _=self.locale.translate,
            pgettext=self.locale.pgettext,
            static_url=self.static_url,
            xsrf_form_html=self.xsrf_form_html,
            reverse_url=self.reverse_url
        )
        # namespace.update(self.ui)
        return namespace

    def jsonify(self, chunk):
        if self._finished:
            raise RuntimeError("Cannot jsonify() after finish().  May be caused "
                               "by using async operations without the "
                               "@asynchronous decorator.")
        chunk = json_encode(chunk)
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        chunk = utf8(chunk)
        self._write_buffer.append(chunk)

    def render(self, template_name, **kwargs):
        """Renders the template with the given arguments as the response."""
        html = self.render_string(template_name, **kwargs)
        self.finish(html)


      
    def Backend(self, key):
        return __backend.get(key)

    def Thing(self, key):
        return __thing.get(key)

    def Model(self, key):
        return __model.get(key)


class RenderHandler(Handler):

    def initialize(self, template):
        self.template = template

    def get(self, *args):
        self.render(self.template)


class SecurityMeta(type):

    def __new__(metacls, cls_name, bases, attrs):
        role = attrs.get('__role__')

        if role:
            prepare = handler_security(role)(Handler.prepare)
            attrs['prepare'] = prepare
            del attrs['__role__']
        cls = type.__new__(metacls, cls_name, bases, attrs)

        return cls


class AssetHandler(StaticFileHandler, Handler):

    def initialize(self):
        self.root = self.application.config.get('content_path')
        self.default_filename = None
