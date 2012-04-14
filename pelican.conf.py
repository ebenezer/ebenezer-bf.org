#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import os
from collections import defaultdict
from itertools import chain

from pelican import Pelican
from pelican.generators import Generator, PagesGenerator, ArticlesGenerator, \
        StaticGenerator, PdfGenerator
from pelican.readers import read_file
from pelican.contents import Page, Category, is_valid_content
from pelican.utils import process_translations


class NewPagesGenerator(Generator):
    """Generate pages"""

    def __init__(self, *args, **kwargs):
        self.pages = []
        self.pages_categories = defaultdict(list)
        super(NewPagesGenerator, self).__init__(*args, **kwargs)
        self.drafts = []

    def generate_context(self):
        all_pages = []

        for f in self.get_files(
                os.path.join(self.path, self.settings['PAGE_DIR']),
                exclude=self.settings['PAGE_EXCLUDES']):
            try:
                content, metadata = read_file(f, settings=self.settings)
            except Exception, e:
                error(u'Could not process %s\n%s' % (f, str(e)))
                continue

            # if no category is set, use the name of the path as a category
            if 'category' not in metadata.keys():

                if os.path.dirname(f) == self.path:
                    category = 'NO_CATEGORY'
                else:
                    category = os.path.basename(os.path.dirname(f)).decode('utf-8')

                if category != '':
                    metadata['category'] = Category(category, self.settings)

            page = Page(content, metadata, settings=self.settings,
                        filename=f)
            if not is_valid_content(page, f):
                continue

            if page.status == "published":
                all_pages.append(page)
            elif page.status == "draft":
                self.drafts.append(page)

        self.pages, self.translations = process_translations(all_pages)

        for page in self.pages:
            # only main pages are listed in pages_categories, not translations
            self.pages_categories[page.category].append(page)

        # order the pages_categories per name
        self.pages_categories = list(self.pages_categories.items())
        self.pages_categories.sort(
                key=lambda item: item[0].name,
                reverse=self.settings['REVERSE_CATEGORY_ORDER'])

        self._update_context(('pages', 'pages_categories',))


    def generate_output(self, writer):
        """Generate the pages on the disk"""

        page_template = self.get_template('page')
        for page in chain(self.translations, self.pages):
            writer.write_file(page.save_as, page_template,
                    self.context, page=page, category=page.category,
                    relative_urls=self.settings.get('RELATIVE_URLS'))
        for page in self.drafts:
            writer.write_file('pages/drafts/%s.html' % page.slug, page_template,
                    self.context, page=page, category=page.category,
                    relative_urls=self.settings.get('RELATIVE_URLS'))

        category_template = self.get_template('page_category')
        for cat, pages in self.pages_categories:
            writer.write_file(cat.save_as, category_template, self.context,
                    category=cat, pages=pages, paginated={'pages': pages, 'articles':[]},
                    relative_urls=self.settings.get('RELATIVE_URLS'))


class MyPelican(Pelican):

    def get_generator_classes(self):
        generators = [ArticlesGenerator, NewPagesGenerator, StaticGenerator]
        if self.settings['PDF_GENERATOR']:
            generators.append(PdfGenerator)
        return generators


PELICAN_CLASS = MyPelican

AUTHOR = u"Bruno Binet"
SITENAME = u"Centre Eben-Ezer"
SITEURL = '/'

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
DEFAULT_PAGINATION = False

STATIC_PATHS = ['data']
OUTPUT_PATH = '_output/'
PAGE_DIR = 'pages'
ARTICLE_DIR = 'news'

ARTICLE_URL = 'actualites/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'actualites/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
PAGE_URL = '{category}/{slug}/'
PAGE_SAVE_AS = '{category}/{slug}/index.html'


THEME = './theme/'
