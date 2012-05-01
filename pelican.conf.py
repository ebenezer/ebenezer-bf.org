#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import os
import re
from operator import attrgetter
from collections import defaultdict
from itertools import chain

import markdown
from pelican import Pelican
from pelican.generators import Generator, PagesGenerator, ArticlesGenerator, \
        StaticGenerator, PdfGenerator
from pelican.readers import read_file, _METADATA_PROCESSORS
from pelican.contents import Page, Category, is_valid_content
from pelican.utils import process_translations
from mdx_video import VideoExtension


_METADATA_PROCESSORS.update({
    'sorting': lambda x, y: int(x),
    })


class PagesCategory(Category):
    def __init__(self, name, settings, title=None):
        super(PagesCategory, self).__init__(name, settings)
        self.title = title if title else name

class NewPagesGenerator(Generator):
    """Generate pages"""

    def __init__(self, *args, **kwargs):
        self.pages = []
        self.all_pages_categories = defaultdict(list)
        super(NewPagesGenerator, self).__init__(*args, **kwargs)
        self.drafts = []

    def generate_context(self):
        all_pages = []

        pagecat_map = dict(self.settings.get('PAGECAT_MAP'))
        for f in self.get_files(
                os.path.join(self.path, self.settings['PAGE_DIR']),
                exclude=self.settings['PAGE_EXCLUDES']):
            try:
                content, metadata = read_file(f, settings=self.settings)
            except Exception, e:
                print(u'Could not process %s\n%s' % (f, str(e)))
                continue

            # if no sorting is set, set default to 99
            if 'sorting' not in metadata.keys():
                metadata['sorting'] = 99

            # if no category is set, use the name of the path as a category
            if 'category' not in metadata.keys():

                if os.path.dirname(f) == self.path:
                    category = 'NO_CATEGORY'
                else:
                    category = os.path.basename(os.path.dirname(f)).decode('utf-8')

                if category != '':
                    title = pagecat_map[category] \
                                if category in pagecat_map else None
                    metadata['category'] = PagesCategory(
                            category, self.settings, title)

            page = Page(content, metadata, settings=self.settings,
                        filename=f)
            if not is_valid_content(page, f):
                continue

            if page.status == "published":
                all_pages.append(page)
            elif page.status == "draft":
                self.drafts.append(page)

        self.pages, self.translations = process_translations(all_pages)

        # sort pages on both 'sorting' and 'title' attribute
        self.pages.sort(key=attrgetter('sorting', 'title'))

        for page in self.pages:
            # only pages are listed in all_pages_categories, not translations
            self.all_pages_categories[page.category].append(page)

        pcats = dict([(cat.name, (cat, pages)) for cat, pages in \
                self.all_pages_categories.iteritems()])

        # create the pages_categories list based on PAGECAT_MAP config
        self.pages_categories = []
        for cat, _ in self.settings.get('PAGECAT_MAP'):
            if cat in pcats:
                self.pages_categories.append(pcats[cat])

        self._update_context(
                ('pages', 'pages_categories', 'all_pages_categories',))


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


# class ReSubPreprocessor(markdown.preprocessors.Preprocessor):
#     def __init__(self, *args, **kwargs):
#         self.pattern, self.repl = kwargs['resub']
#         del kwargs['resub']
#         markdown.preprocessors.Preprocessor.__init__(self, *args, **kwargs)
#     def run(self, lines):
#         new_lines = []
#         for line in lines:
#             new_lines.append(re.sub(self.pattern, self.repl, line))
#         return new_lines
# class ReSubExtension(markdown.Extension):
#     def extendMarkdown(self, md, md_globals):
#         md.preprocessors.insert(0, 'resub', ReSubPreprocessor(md, **self.config))
# llink = ReSubExtension(configs={'resub': ('\]: /_/', ']: /PREFIX_TEST/')})


class MyPelican(Pelican):

    def get_generator_classes(self):
        generators = [ArticlesGenerator, NewPagesGenerator, StaticGenerator]
        if self.settings['PDF_GENERATOR']:
            generators.append(PdfGenerator)
        return generators


PELICAN_CLASS = MyPelican
MD_EXTENSIONS = ['codehilite', 'extra', VideoExtension({})]

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

STATIC_PATHS = ['data']
OUTPUT_PATH = '_output/'
PAGE_DIR = 'pages'
ARTICLE_DIR = 'news'

ARTICLE_URL = 'actualites/{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = 'actualites/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
PAGE_URL = '{category}/{slug}/'
PAGE_SAVE_AS = '{category}/{slug}/index.html'
PAGESCATEGORY_URL = 'category/{slug}/'
PAGESCATEGORY_SAVE_AS = 'category/{slug}/index.html'

PAGECAT_MAP = [
        (u'centre-ebenezer', u'Centre Eben-Ezer'),
        (u'centre-scolaire', u'Centre Scolaire'),
        (u'partenaires', u'Partenaires'),
        (u'temple-eternel', u'Temple de l\'Éternel'),
        (u'a-propos', u'A propos'),
        ]


THEME = './theme/'
GOOGLE_ANALYTICS = 'UA-31288611-1'
