from webpush_channels import __version__ as VERSION
from kinto.core.testing import unittest
from .support import BaseWebTest

class HelloViewTest(BaseWebTest, unittest.TestCase):

	def test_returns_info_about_url_and_version(self):
		response = self.app.get('/')
        self.assertEqual(response.json['version'], VERSION)
        self.assertEqual(response.json['url'], 'http://localhost/v1/')
        self.assertEqual(response.json['hello'], 'webpush-channels')
        self.assertEqual(response.json['documentation'],
                         'http://webpush-channels-broadcasting.readthedocs.io/')


		