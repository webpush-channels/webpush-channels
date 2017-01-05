import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

with open(os.path.join(here, 'CHANGELOG.rst')) as f:
    CHANGELOG = f.read()


REQUIREMENTS = [
    'waitress',
    'kinto.core',
    'requests'
]

ENTRY_POINTS = {
    'paste.app_factory': [
        'main = webpush-channels:main',
    ]}

setup(name='webpush-channels',
      version='1.0.0.dev0',
      description='Broadcast notifications to multiple WebPush subscribers.',
      long_description=README + "\n\n" + CHANGELOG,
      keywords="webpush notifications, webpush channels",
      author='Mansimar Kaur',
      author_email='mansimarkaur.mks@gmail.com',
      url='http://webpush-channels-broadcasting.readthedocs.io/en/latest/',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=REQUIREMENTS,
      entry_points=ENTRY_POINTS)
