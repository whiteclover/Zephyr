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


import logging
from sys import exc_info


LOGGER = logging.getLogger('seraph.hook')

class Hook(object):

    """A callback and its metadata: failsafe, priority, and kwargs."""

    callback = None
    """
    The bare callable that this Hook object is wrapping, which will
    be called when the Hook is called."""

    failsafe = False
    """
    If True, the callback is guaranteed to run even if other callbacks
    from the same call point raise exceptions."""

    priority = 50
    """
    Defines the order of execution for a list of Hooks. Priority numbers
    should be limited to the closed interval [0, 100], but values outside
    this range are acceptable, as are fractional values."""


    def __init__(self, callback, failsafe=None, priority=None):
        self.callback = callback

        if failsafe is None:
            failsafe = getattr(callback, "failsafe", False)
        self.failsafe = failsafe

        if priority is None:
            priority = getattr(callback, "priority", 50)
        self.priority = priority

    def __lt__(self, other):
        # Python 3
        return self.priority < other.priority

    def __cmp__(self, other):
        # Python 2
        return cmp(self.priority, other.priority)

    def __call__(self, *args, **kw):
        """Run self.callback(*args, **kw)."""
        return self.callback(*args, **kw)

    def __repr__(self):
        cls = self.__class__
        return ("%s.%s(callback=%r, failsafe=%r, priority=%r)"
                % (cls.__module__, cls.__name__, self.callback,
                   self.failsafe, self.priority))


class HookMap(dict):

    """A map of call points to lists of callbacks (Hook objects)."""

    def __new__(cls, points=None):
        d = dict.__new__(cls)
        for p in points or []:
            d[p] = []
        return d

    def __init__(self, *a, **kw):
        pass

    def attach(self, point, callback, failsafe=None, priority=None, **kwargs):
        """Append a new Hook made from the supplied arguments."""
        if point not in self:
            self[point] = []
        self[point].append(Hook(callback, failsafe, priority, **kwargs))
        self[point].sort()

    def run(self, point, *args, **kw):
        """Execute all registered Hooks (callbacks) for the given point."""
        exc = None
        hooks = self.get(point, [])
        for hook in hooks:
            # Some hooks are guaranteed to run even if others at
            # the same hookpoint fail. We will still log the failure,
            # but proceed on to the next hook. The only way
            # to stop all processing from one of these hooks is
            # to raise SystemExit and stop the whole server.
            if exc is None or hook.failsafe:
                try:
                    hook(*args, **kw)
                except (KeyboardInterrupt, SystemExit):
                    raise
                except:
                    exc = exc_info()[1]
                    LOGGER.exception("Hook Error: %s", exc)
        if exc:
            raise exc

    def __copy__(self):
        newmap = self.__class__()
        # We can't just use 'update' because we want copies of the
        # mutable values (each is a list) as well.
        for k, v in self.items():
            newmap[k] = v[:]
        return newmap
    copy = __copy__

    def __repr__(self):
        cls = self.__class__
        return "%s.%s(points=%r)" % (
            cls.__module__,
            cls.__name__,
            self.keys()
        )