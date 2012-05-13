from pelican.contents import Category

class PagesCategory(Category):
    def __init__(self, name, settings, title=None):
        super(PagesCategory, self).__init__(name, settings)
        self.title = title if title else name

