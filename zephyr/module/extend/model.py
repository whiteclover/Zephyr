
__all__ = ['Extend', 'Meta', 'Field']


from zephyr.util import markdown
from zephyr.jinja2t import Markup

class Extend(object):

    def __init__(self, type, key, label, field, attributes, eid=None):
        """The Extend simple model"""
        self.key = key
        self.label = label
        self.type = type
        self.field = field
        self.attributes = attributes or {}

        if eid:
            self.eid = eid

    def value(self, node_id, type='post'):
        meta = Backend('Meta').find(type, node_id, self.eid)
        meta = meta or Meta(node_id, type, self.eid)
        return Field(self, meta)

    def __str__(self):
        return "<Extend key:%s, label:%s>" %(self.key, self.label)


class Meta(object):

    def __init__(self, node_id, type, extend, data=None, mid=None):
        self.node_id = node_id
        self.type = type
        self.extend = extend
        self.data = data or {}
        if mid:
            self.mid = mid

    def get(self, key, default=None):
        return self.data.get(key, default)


class Field(object):

    def __init__(self, extend, meta):
        self.extend = extend
        self.meta = meta

    def value(self):
        field = self.field
        if field == 'text':
            value = self.meta.get('text', '')
        elif field == 'html':
            value = markdown(self.meta.get('html', ''))
        elif field in ('image', 'file'):
            f = self.meta.get('filename', '')
            if f:
                value = '/content/' + f
            else:
                value = ''
        return Markup(value)
        

    @property
    def field(self):
        return self.extend.field

    @property
    def key(self):
        return self.extend.key

    @property
    def label(self):
        return self.extend.label

    def __html__(self):
        field = self.field
        if field == 'text':
            value = self.meta.get('text', '')
            return '<input id="extend_"' + self.key + '" name="extend_' + self.key + \
                 '" type="text" value="' + value + '">'

        if field == 'html':
            value = self.meta.get('html', '')
            return '<textarea id="extend_' + self.key + '" name="extend_' + self.key + \
                '" type="text">' + value + '</textarea>'

        if field in ('file', 'image'):
            value = self.meta.get('filename', '')
            html = '<span class="current-file">'

            if value:
                html += '<a href="' + '/assets/content/' + value + '" target="_blank">' + value + '</a>'

            html += '</span><span class="file"> <input id="extend_' + self.key + '" name="extend_' + \
                    self.key + '" type="file"> </span>'

            return html

        return ''

    html  = __html__
