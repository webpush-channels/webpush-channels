from webpush_channels import __version__ as VERSION
from kinto.core.testing import unittest
from .support import BaseWebTest

class HelloViewTest(BaseWebTest, unittest.TestCase):
	def test_returns_info_about_url_and_version(self):
		response = self.app.get('/')
		self.assertEqual(response.json['project_name'], 'webpush-channels')
		self.assertEqual(response.json['project_version'], VERSION)
		self.assertEqual(response.json['project_docs'],
                         'http://webpush-channels-broadcasting.readthedocs.io/')
		self.assertEqual(response.json['url'], 'http://localhost:9999/v0/')
