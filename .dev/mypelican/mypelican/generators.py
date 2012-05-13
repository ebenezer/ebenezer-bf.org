# -*- coding: utf-8 -*- #
import os
from operator import attrgetter
from collections import defaultdict
from itertools import chain

from pelican.generators import Generator
from pelican.readers import read_file, _METADATA_PROCESSORS
from pelican.contents import Page, Category, is_valid_content
from pelican.utils import process_translations
from mypelican.contents import PagesCategory

_METADATA_PROCESSORS.update({
    'sorting': lambda x, y: int(x),
    })

class NewPagesGenerator(Generator):
    """Generate pages"""

    def __init__(self, *args, **kwargs):
        self.pages = []
        self.all_pages_categories = defaultdict(list)
        super(NewPagesGenerator, self).__init__(*args, **kwargs)
        self.ignored_pages = []

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

            # all pages which status is not "published" will be ignored
            if page.status == "published":
                all_pages.append(page)
            else:
                self.ignored_pages.append(page)

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

        self._update_context(('pages', 'ignored_pages', 'pages_categories',
            'all_pages_categories',))


    def generate_output(self, writer):
        """Generate the pages on the disk"""

        page_template = self.get_template('page')
        for page in chain(self.translations, self.pages):
            writer.write_file(page.save_as, page_template,
                    self.context, page=page, category=page.category,
                    relative_urls=self.settings.get('RELATIVE_URLS'))

        category_template = self.get_template('page_category')
        for cat, pages in self.pages_categories:
            writer.write_file(cat.save_as, category_template, self.context,
                    category=cat, pages=pages, paginated={'pages': pages, 'articles':[]},
                    relative_urls=self.settings.get('RELATIVE_URLS'))

