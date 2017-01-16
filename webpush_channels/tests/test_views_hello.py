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
        self.assertEqual(response.json['url'], 'http://localhost/v0/')


class LoadBalancerHeartbeat(BaseWebTest, unittest.TestCase):
    def test_checks_if_lheartbeat_is_working(self):
        resp = self.app.get('/__lbheartbeat__')
        self.assertEqual(resp.json, {})


class Heartbeat(BaseWebTest, unittest.TestCase):
    def test_returns_storage_true_if_ok(self):
        response = self.app.get('/__heartbeat__')
        self.assertEqual(response.json['storage'], True)

    def test_returns_cache_true_if_ok(self):
        response = self.app.get('/__heartbeat__')
        self.assertEqual(response.json['cache'], True)

    def test_successful_if_one_heartbeat_is_none(self):
        self.app.app.registry.heartbeats['probe'] = lambda r: None
        response = self.app.get('/__heartbeat__', status=200)
        self.assertEqual(response.json['probe'], None)
