
import base64
import uuid
from hashlib import sha224

from datetime import datetime


__all__ = ['User']

class User(object):


    def __init__(self, username, email, real_name, password, salt, bio, status, role='user', uid=None):
        """If the user load from database, if will intialize the uid and secure password.
        Otherwise will hash encrypt the real password

        arg role enum: the string in ('root', 'user', 'editor', 'administrator')
        arg status enum: the string in ('active', 'inactive')
        arg password fix legnth string: the use sha224 password hash
        """
        self.username = username
        self.email = email
        self.real_name = real_name
        self.bio = bio
        self.status = status
        self.role = role

        self.uid = uid
        if self.uid is not None:
            self._secure_pass = password
            self.secure_salt = salt
        else:
            self.secure_salt = self.gen_salt()
            self._secure_pass = self.secure_password(password)

  
    def inactive(self):
        return self.status == 'inactive'

    def gen_salt(self):
        return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)

    def secure_pass():
        doc = "The secure_pass property."
        def fget(self):
            return self._secure_pass
        def fset(self, value):
            self._secure_pass = self.secure_password(value)
        def fdel(self):
            del self._secure_pass
        return locals()
    secure_pass = property(**secure_pass())

    def secure_password(self, password):
        """Encrypt password to sha224 hash"""
        return sha224(self.secure_salt + password).hexdigest()

    def check(self, password):
        return self.secure_pass == self.secure_password(password)