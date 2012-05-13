import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'pelican',
    'Markdown',
    'ghp-import',
    ]

setup(name='mypelican',
      version='0.0',
      description='mypelican',
      long_description='my pelican',
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
        ],
      author='Bruno Binet',
      author_email='binet.bruno@gmail.com',
      url='',
      keywords='web static website generator pelican',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      )

