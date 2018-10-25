#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Andreu Vallbona'
SITENAME = 'Andreu Vallbona'
SITESUBTITLE = ''
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Madrid'

DEFAULT_LANG = 'en'
DEFAULT_DATE_FORMAT = '%B %d, %Y'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         # ('You can modify those links in your config file', '#'),
         )

# Social widget
SOCIAL = (('github', 'https://github.com/avallbona'),
          ('twitter', 'https://twitter.com/avallbona'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

THEME = 'themes/halcyonic'

STATIC_PATHS = ['static']

PLUGIN_PATHS = ['/var/www/pelican-plugins']
PLUGINS = ['neighbors']

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""

