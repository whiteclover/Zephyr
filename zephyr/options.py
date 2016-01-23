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


from argparse import ArgumentParser
import sys

from zephyr.config import ConfigFactory


class Options(object):

    def __init__(self, help_doc=None,  args=sys.argv):
        self.args = args
        if help_doc is None:
            self.argparser = ArgumentParser(add_help=False)
        else:
            self.argparser = ArgumentParser(help_doc)

    def group(self, help_doc):
        group_parser = self.argparser.add_argument_group(help_doc)
        return GroupOptions(group_parser)

    def set_defaults(self, **c):
        self.argparser.set_defaults(**c)

    @property
    def define(self):
        return self.argparser.add_argument

    def parse_args(self, args=None):
        args = args if args is not None else self.args
        opt, _ = self.argparser.parse_known_args(args)
        return opt


class GroupOptions(object):

    def __init__(self, group_parser):
        self.group_parser = group_parser

    @property
    def define(self):
        return self.group_parser.add_argument

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

__options = None


def setup_options(doc):
    global __options
    __options = Options(doc)


def group(help_doc):
    return __options.group(help_doc)


def define(*args, **kw):
    return __options.define(*args, **kw)


def set_defaults(**c):
    __options.set_defaults(**c)


def parse_args():
    return __options.parse_args()
