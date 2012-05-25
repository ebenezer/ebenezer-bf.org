#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from mypelican import MyPelican


PELICAN_CLASS = MyPelican
MD_EXTENSIONS = ['codehilite', 'extra', 'video(youtube_width=700, youtube_height=595)']

AUTHOR = 'Issa Ouedraogo'
SITENAME = 'Centre Eben-Ezer'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG='fr'

# Blogroll
LINKS =  (
        ('Au Coeur du Sahel', 'http://dedougou.ovh.org/'),
         )

# Social widget
# SOCIAL = (
#           ('You can add links in your config file', '#'),
#          )

DISPLAY_PAGES_ON_MENU = True
DEFAULT_PAGINATION = 5

# STATIC_PATHS = ['data']
OUTPUT_PATH = '_output/'
PAGE_DIR = 'pages'
ARTICLE_DIR = 'news'

ARTICLE_URL = 'actualites/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'actualites/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
PAGE_URL = '{category}/{slug}/'
PAGE_SAVE_AS = '{category}/{slug}/index.html'
PAGESCATEGORY_URL = 'category/{slug}/'
PAGESCATEGORY_SAVE_AS = 'category/{slug}/index.html'

DIRECT_TEMPLATES = ('index', 'articles', 'tags', 'archives',)
PAGINATED_DIRECT_TEMPLATES = ('articles',)
ARTICLES_SAVE_AS = 'actualites/index.html'
TAGS_SAVE_AS = 'actualites/tags/index.html'
ARCHIVES_SAVE_AS = 'actualites/archives/index.html'

PAGECAT_MAP = [
        (u'centre-ebenezer', u'Centre Eben-Ezer'),
        (u'centre-scolaire', u'Centre Scolaire'),
        (u'partenaires', u'Partenaires'),
        (u'temple-eternel', u'Temple de l\'Éternel'),
        (u'a-propos', u'A propos'),
        ]


THEME = './.dev/theme/'
GOOGLE_ANALYTICS = 'UA-31288611-1'
DISQUS_SITENAME = 'ebenezer-bf'
