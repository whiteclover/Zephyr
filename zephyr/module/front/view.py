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

from zephyr.breeze import Backend, Thing, AssetHandler


def front_menu(m):
    r = m.r
    m.connect(r'/content/(.*)', AssetHandler)
    m.connect(r'/', FrontPage, name='site_page')
    m.connect(r('/<slug>'), FrontPage)
    m.connect(r('/post/<slug>'), SlugPostPage, name='site_post')
    m.connect(r'/posts', PostPage)
    m.connect(r('/posts/<page:int>'), PostPage)
    m.connect(r('/posts/<category>'), PostPage)
    m.connect(r('/posts/<category>/<page:int>'), PostPage)
    m.connect(r'/feed/rss.json', FeedPage)
    m.connect(r'/feed/rss', FeedXMLPage)
    m.connect(r('/post/comment/<slug>'), PostComment)


from .mixin import FeedMixin, FrontMixin
from zephyr.helper import site


class FrontPage(FrontMixin, FeedMixin):

    def get(self, slug=None):
        if slug:
            if slug == 'admin':
                return self.post_admin_page()
            elif slug == 'search':
                return self.search()
            elif slug == 'rss':
                return self.feed_rss()

            slug = slug.split('/')[-1]
            page = self.page_service.get_by_slug(slug)
        else:
            site_page = site.get('site_page', 0)
            if site_page == 0:
                return self.posts()
            else:
                page = self.page_service.get(site_page)

        if not page:
            self.notfound()
        self.theme_render('page.html',
                          page_content=page.content,
                          page_title=page.title,
                          page=page)


class PostComment(FrontMixin):

    def post(self, slug):
        self.post_comment(slug)


class PostPage(FrontMixin):

    def get(self, page=1, category=None):
        page = int(page)
        self.posts(page, category)


class SlugPostPage(FrontMixin):

    def get(self, slug):
        self.post_page(slug)


class FeedPage(FeedMixin):

    def get(self):
        self.feed_json()


class FeedXMLPage(FeedMixin):

    def get(self):
        self.feed_rss()
