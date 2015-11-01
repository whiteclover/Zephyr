__all__ = ['Page']


from zephyr.breeze import Backend

class Page(object):

    def __init__(self, parent, name, title, slug, content, status, redirect, show_in_menu, pid=None):

        self.parent = parent
        self.name = name
        self.title = title
        self.slug = slug
        self.content = content
        self.status = status
        self.redirect = redirect
        self.show_in_menu = show_in_menu
        if pid:
            self.pid = pid


    def custom_field(self, key):
        extend = Backend('extend').field('page', key)
        return extend.value(self.pid, type='page')

    def url(self):
        segments = [self.slug]
        parent = self.parent
        Store = Backend('page')
        while parent:
            page = Store.find(parent)
            if page:
                segments.insert(0, page.slug)
                parent = page.parent
            else:
                break

        return '/' + '/'.join(segments)