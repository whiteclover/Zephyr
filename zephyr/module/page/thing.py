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


from .model import Page

from zephyr.breeze import Backend
from zephyr.lib.paginator import Paginator
from zephyr.lang import text


__all__ = ['PageThing']

class PageThing(object):

    def __init__(self):
        self.page_repo = Backend(Page.__name__)

    get = lambda self, pid: self.page_repo.find(pid)

    def get_by_redirect(self, redirect):
        return self.page_repo.find_by_redirect(redirect)

    def get_by_slug(self, slug):
        return self.page_repo.find_by_slug(slug)

    def dropdown(self, show_in_menu=True):
        return self.page_repo.dropdown(show_in_menu)

    def page(self, status, page=1, perpage=10):
        total = self.page_repo.count(status)
        pages = self.page_repo.paginate(page, perpage, status)
        if status:
            url = '/admin/page/status/' + status
        else:
            url = '/admin/page'
        pagination = Paginator(pages, total, page, perpage, url)
        return pagination

    def delete(self, page_id):
        page = self.page_repo.find(page_id)
        if not page:
            return None
        return self.page_repo.delete(page.pid)

    def add_page(self, parent, name, title, slug, content, status, redirect, show_in_menu):
        redirect = redirect.strip()
        show_in_menu = 1 if show_in_menu else 0
        page = Page(parent, name, title, slug, content, status, redirect, show_in_menu)
        pid = self.page_repo.create(page)
        page.pid = pid
        return page

    def is_exist_slug(self, slug):
        return self.page_repo.count_slug(slug) == 1

    def update_page(self, parent, name, title, slug, content, status, redirect, show_in_menu, pid):
        show_in_menu = 1 if show_in_menu else 0
        redirect = redirect.strip()
        page = Page(parent, name, title, slug, content, status, redirect, show_in_menu, pid)
        self.page_repo.save(page)
        return page
