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


from zephyr.jinja2t import Markup


class Paginator(object):

    def __init__(self, results, total, page, perpage, url, glue='/'):
        self.results = results
        self.total = total
        self.page = page
        self.first = 'First'
        self.last = 'Last'
        self._next = 'Next'
        self._prev = 'Previous'
        self.perpage = perpage
        self.url = url
        self._index = 0
        self.glue = glue

    def next_link(self,  text='&larr; Previous', default=''):
        text = text or self._next
        pages = (self.total / self.perpage) + 1
        if self.page < pages:
            page = self.page + 1
            return '<a href="' + self.url + self.glue + str(page) + '">' + text + '</a>'

        return default

    def pre_link(self, text='&larr; Previous', default=''):
        text = text or self._prev
        if self.page > 1:
            page = self.page - 1
            return Markup('<a href="' + self.url + self.glue + str(page) + '">' + text + '</a>')

        return Markup(default)

    def links(self):
        html = ''
        pages = (self.total / self.perpage)
        if self.total % self.perpage != 0:
            pages += 1
        ranged = 4
        if pages > 1:
            if self.page > 1:
                page = self.page - 1
                html += '<a href="' + self.url + '">' + self.first + '</a>' + \
                    '<a href="' + self.url + self.glue + str(page) + '">' + self._prev + '</a>'
            for i in range(self.page - ranged, self.page + ranged):
                if i < 0:
                    continue
                page = i + 1
                if page > pages:
                    break

                if page == self.page:
                    html += '<strong style="color:black">' + str(page) + '</strong>'
                else:
                    html += '<a href="' + self.url + self.glue + str(page) + '">' + str(page) + '</a>'

            if self.page < pages:
                page = self.page + 1

                html += '<a href="' + self.url + self.glue + str(page) + '">' + self._next + '</a> <a href="' + \
                    self.url + self.glue + str(pages) + '">' + self.last + '</a>'

        return html

    __html__ = links

    def __len__(self):
        return len(self.results)

    def __iter__(self):
        return self

    def next(self):
        try:
            result = self.results[self._index]
        except IndexError:
            raise StopIteration
        self._index += 1
        return result

    __next__ = next  # py3 compat
