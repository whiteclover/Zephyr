
__all__ = ['Pair']


from tornado.escape import json_decode

class Pair(object):

    def __init__(self, key, value):
        self.key = key
        self.value = value 

    def json_value(self):
        return json_decode(self.value)