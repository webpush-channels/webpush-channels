import unittest
from .support import BaseWebTest


class ChannelRegistrationTest(BaseWebTest, unittest.TestCase):
    channel_url = '/channels/food'
    channel_registration_url = '/channels/food/registration'

    def setUp(self):
        super(ChannelRegistrationTest, self).setUp()

    def test_registration_can_be_added_for_a_user(self):
        self.app.put(self.channel_registration_url, headers=self.headers, status=202)
        resp = self.app.get(self.channel_url, headers=self.headers, status=200)
        assert resp.json['data']['registrations'] == 1

    def test_registration_can_be_remove_for_a_user(self):
        self.app.put(self.channel_registration_url, headers=self.headers, status=202)
        self.app.delete(self.channel_registration_url, headers=self.headers, status=202)
        resp = self.app.get(self.channel_url, headers=self.headers, status=200)
        assert resp.json['data']['registrations'] == 0


class ChannelsTest(BaseWebTest, unittest.TestCase):
    channel_url = '/channels/food'

    def setUp(self):
        super(ChannelsTest, self).setUp()

    def test_channels_information_can_be_retrieved(self):
        resp = self.app.get(self.channel_url, headers=self.headers, status=200)
        assert 'data' in resp.json

        assert 'registrations' in resp.json['data']
        assert 'push' in resp.json['data']

        assert resp.json['data']['registrations'] == 0
        assert resp.json['data']['push'] == 0
