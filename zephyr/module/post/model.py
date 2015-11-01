from zephyr.breeze import Backend
from zephyr.helper import cached_user
from zephyr.util import lazy_attr


__all__ = ['Post']

class Post(object):

    def __init__(self, title, slug, description, html, css, js, category, status, allow_comment, 
        author=None, updated=None, created=None, pid=None):
        self.title = title
        self.slug = slug
        self.description = description


        self.html = html
        self.css = css
        self.js = js
        self.category = category
        self.status = status
        self.allow_comment = allow_comment
        self.author = author
        self.pid = pid

        self.updated = updated or datetime.now()
        self.created = created or datetime.now()


    @property
    def user(self):
        return cached_user(self.author)

    @lazy_attr
    def comments(self):
        return Backend('Comment').find_by_post_id(self.pid)


    def __json__(self):
        data = self.__dict__.copy()
        del data['js']
        del data['css']
        del data['slug']
        del data['commments']
        return data


    def custom_field(self, key):
        extend = Backend('extend').field('post', key)
        return extend.value(self.pid, type='post')
