import tornado.web

from .hook import HookMap


class Application(tornado.web.Application):

    hookpoints = ['on_start_request', 'on_end_request',
                'before_error_response', 'after_error_response']

    def __init__(self, handlers, **settings):
        self.error_pages = {}
        self.hooks = HookMap()
        tornado.web.Application.__init__(
            self, handlers, **settings)

    def attach(self, point, callback, failsafe=None, priority=None, **kwargs):
        if point not in self.hookpoints:
            return
        self.hooks.attach(point, callback, failsafe, priority, **kwargs)

    def error_page(self, code, callback):
        if type(code) is not int:
            raise TypeError("code:%d is not int type" % (code))
        self.error_pages[str(code)] = callback
