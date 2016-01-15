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


from datetime import datetime
from urlparse import urljoin

from tornado.web import HTTPError
from zephyr.breeze import Backend, Thing
from zephyr.feed import AtomFeed
from zephyr.helper import site
from zephyr.lang import text
from zephyr.lib.memoize import memoize
from zephyr.lib.validator import Validator
from zephyr.util import markdown

class ServiceMixin:
    """services"""
    post_service = Thing('Post')
    category_service = Thing('Category')
    comment_service = Thing('Comment')
    page_service = Thing('Page')


class FrontMixin(ServiceMixin):

    def posts(self, page=1, category=None):
        if page <= 0:
            return self.theme_render(self, '404.html')
        total, posts = self.post_service.get_published_posts_page(
            page, site.posts_per_page(), category)
        self.theme_render('posts.html',
                          page_title='posts',
                          post_total=total,
                          posts=posts,
                          page_offset=page)

    def theme_render(self, tpl, *args, **kw):
        theme = self.application.config.get('theme', 'default')
        tpl = 'theme/' + theme + '/' + tpl
        return self.render(tpl, *args, **kw)

    def post_page(self, slug):
        post = self.post_service.get_by_slug(slug)
        if not post:
            return self.theme_render('404.html')

        self.theme_render('article.html',
                          page_title=post.title,
                          article=post,
                          comments=post.comments,
                          category=self.category_service.get_by_cid(post.category))

    def post_admin_page(self):
        pagination = self.post_service.page(1, site.posts_per_page(), category)
        self.render('admin//post/index.html',
                    categories=self.category_service.dropdown(),
                    posts=pagination,
                    category=category)

    def page_redirect(self):
        path = self.request.path
        page = self.page_service.get_by_redirect(path)
        if not page:
            return self.theme_render('404.html', page_title='Not Found')
        self.theme_render('page.html',
                          page_content=page.content,
                          page_title=page.title,
                          page=page)

    def search(self):
        key = self.get_argument('q')
        page = int(self.get_argument('page', default=1))
        pages = self.post_service.search(key, page)

        self.theme_render('search.html',
                          page_title='Serach Article',
                          search_term=key,
                          articles=pages)

    def post_comment(self, slug):
        post = self.post_service.get_by_slug(slug)
        if not post:
            return self.theme_render('404.html', page_title='Not Found')

        if post and not post.allow_comment:
            return self.redirect(self.reverse_url('site_post', slug))

        p = self.get_argument
        name = p('name', default='')
        email = p('email', default='')
        content = p('content', default='')

        name, content, email = name.strip(), content.strip(), email.strip()

        validator = Validator()
        (validator.check(email, 'email', text('comment.email_missing'))
            .check(content, 'min', text('comment.email_missing'), 1)
         )

        if validator.errors:
            self.flash(validator.errors, 'error')
            return redirect(self.reverse_url('site_post', slug))

        status = site.get(
            'auto_published_comments', False) and 'approved' or 'pending'
        self.comment_service.add_comment(name, email, content, status, post)

        self.redirect(self.reverse_url('site_post', slug))

    def notfound(self):
       raise HTTPError(status_code=404, log_message='Not Found')


class FeedMixin:

    def feed_rss(self):
        self.set_header('Content-Type', 'application/xml')
        self.write(_feed_rss(self.url('')))

    def feed_json(self):
        self.jsonify(_feed_json(self.url('feed/rss.json')))

    def url(self, path):
        return ("%s://%s/%s" %
                (self.request.protocol,
                 self.request.host, path)
                )


@memoize(lifetime=30 * 60)
def _feed_rss(url):
    feed = AtomFeed(title=site.sitename(), subtitle='Recent Articles',
                    feed_url=url + 'feed/rss', url=url, updated=datetime.now())

    for post in ServiceMixin.post_service.get_published_posts():
        feed.add(post.title, markdown(post.html),
                 content_type='html',
                 author=post.user.username,
                 url=url + 'post/' + post.slug,
                 updated=post.updated,
                 published=post.created)
    return ''.join(feed.generate())


@memoize(lifetime=30 * 60)
def _feed_json(url):
    posts = []
    for post in ServiceMixin.post_service.get_published_posts():
        data = dict(author=post.user.username,
                    html=markdown(post.html),
                    url=urljoin( url , '/post/' + post.slug),
                    updated=post.updated,
                    published=post.created
                    )
        posts.append(data)

    rss = {
        'sitename': site.sitename(),
        'site': url,
        'updated': datetime.now(),
        'description': site.description(),
        'posts': posts
    }
    return rss
