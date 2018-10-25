#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# Various python modules needed for the theme to function properly (specifically, jinja filters)

import sys
from datetime import datetime

sys.path.append('.')
from utils import filters

JINJA_FILTERS = {'ordinal': filters.ordinal}
COPYRIGHT_YEAR = datetime.now().strftime('%Y')

SITENAME = 'Andreu Vallbona'
AUTHOR = 'Pelican'
SITEDESCRIPTION = 'An HTML5 UP Theme'
SITEURL = ''
DEFAULT_DATE_FORMAT = "%B %-d, %Y"
PATH = 'content'
STATIC_PATHS = ['images']
TIMEZONE = 'Europe/Madrid'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Top Nav menu
MENUITEMS = (
    ('About me', '/about-me'),
    ('Tags', '/tags'),
    ('Categories', '/categories'),
    ('Archives', '/archives'),
)

# Social widget
SOCIAL = (
    ('LinkedIn', 'https://www.linkedin.com/in/andreu-vallbona-plazas-b0b58720'),
    ('Twitter', 'https://twitter.com/avallbona'),
)

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
THEME = 'themes/halcyonic'
PLUGIN_PATHS = ['/var/www/pelican-plugins']
PLUGINS = ['plugins/neighbors']

ARTICLE_URL = 'blog/{slug}'
ARTICLE_SAVE_AS = 'blog/{slug}.html'
PAGE_URL = '{slug}'
PAGE_SAVE_AS = '{slug}.html'
CATEGORY_URL = 'category/{slug}'
CATEGORY_SAVE_AS = 'category/{slug}.html'
TAG_URL = 'tag/{slug}'
TAG_SAVE_AS = 'tag/{slug}.html'
# Uncomment and edit with your GA id to enable Google Analytics
# GOOGLE_ANALYTICS = '86-7530-9'
