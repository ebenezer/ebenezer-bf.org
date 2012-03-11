#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u"Bruno Binet"
SITENAME = u"Centre Eben-Ezer"
SITEURL = '/'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG='fr'

# Blogroll
LINKS =  (
    ('Pelican', 'http://docs.notmyidea.org/alexis/pelican/'),
    ('Python.org', 'http://python.org'),
    ('Jinja2', 'http://jinja.pocoo.org'),
    ('You can modify those links in your config file', '#')
         )

# Social widget
SOCIAL = (
          ('You can add links in your config file', '#'),
         )

DISPLAY_PAGES_ON_MENU = False
DEFAULT_PAGINATION = False

STATIC_PATHS = ['data']
OUTPUT_PATH = '_output/'
PAGE_DIR = 'pages'
ARTICLE_DIR = 'news'

THEME = './theme/'
