#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Tal Leming'
SITENAME = u'The OpenType Cookbook'
SITEURL = 'http://opentypecookbook.com'

GOOGLE_ANALYTICS = "UA-37604844-2"

PATH = 'content'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = u'en'

GITHUB_URL = 'https://github.com/typesupply/opentype-feature-intro'

DEFAULT_PAGINATION = False

MD_EXTENSIONS = ['headerid']

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = 'theme/'

# Pages are more important that articles for OpenType Cookbook.
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'
PAGE_PATHS = ['']
ARTICLE_PATHS = ['nopath']

# Don't generate these defaults pages
ARTICLE_SAVE_AS = ''
ARTICLE_LANG_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
TAG_SAVE_AS = ''
AUTHOR_SAVE_AS = ''
YEAR_ARCHIVE_SAVE_AS = ''
MONTH_ARCHIVE_SAVE_AS = ''
DAY_ARCHIVE_SAVE_AS = ''
ARCHIVES_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
TAGS_SAVE_AS = ''
INDEX_SAVE_AS = ''

FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

TYPOGRIFY = False
