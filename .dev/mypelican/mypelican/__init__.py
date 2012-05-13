# -*- coding: utf-8 -*- #
from pelican import Pelican
from pelican.generators import ArticlesGenerator, StaticGenerator, PdfGenerator

from mypelican.generators import NewPagesGenerator

class MyPelican(Pelican):

    def get_generator_classes(self):
        generators = [ArticlesGenerator, NewPagesGenerator, StaticGenerator]
        if self.settings['PDF_GENERATOR']:
            generators.append(PdfGenerator)
        return generators

