import os
from setuptools import setup, find_packages
import codecs

here = os.path.abspath(os.path.dirname(__file__))

def read_file(filename):
    """Open a related file and return its content."""
    with codecs.open(os.path.join(here, filename), encoding='utf-8') as f:
        content = f.read()
    return content

README = read_file("README.rst")
CHANGELOG = read_file("CHANGELOG.rst")

REQUIREMENTS = [
    'waitress',
    'kinto[postgresql]<6',
    'requests<2.13.0',
    'pywebpush>=0.7.0'
]

ENTRY_POINTS = {
    'paste.app_factory': [
        'main = webpush_channels:main',
    ]}

setup(name='webpush-channels',
      version='0.1.0',
      description='Broadcast notifications to multiple WebPush subscribers.',
      long_description=README + "\n\n" + CHANGELOG,
      license='Apache License (2.0)',
      keywords="webpush notifications, webpush channels",
      author='Mansimar Kaur',
      author_email='mansimarkaur.mks@gmail.com',
      url='https://github.com/webpush-channels/webpush-channels',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=REQUIREMENTS,
      entry_points=ENTRY_POINTS)
