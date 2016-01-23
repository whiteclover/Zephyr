
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


import redis


__redis = {}


def setup(host='localhost', port=6379, db=0, max_connections=None, key='default', password=None, socket_timeout=None,  **connection_kwargs):
    pool = redis.ConnectionPool(host=host, port=port, db=db, max_connections=max_connections, password=password, socket_timeout=socket_timeout, **connection_kwargs)
    __redis[key] = redis.Redis(connection_pool=pool)


def db(key='default'):
    return __redis[key]
