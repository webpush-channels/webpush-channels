import unittest
import mock
from .support import BaseWebTest
from kinto.core.storage import exceptions as storage_exceptions


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

    def test_remove_non_existent_registration(self):
        self.app.delete(self.channel_registration_url, headers=self.headers, status=202)

    def test_we_cannot_register_an_anonymous_user(self):
        self.app.put(self.channel_registration_url, status=401)

    def test_we_cannot_unregister_an_anonymous_user(self):
        self.app.delete(self.channel_registration_url, status=401)


class BackendErrorTest(BaseWebTest, unittest.TestCase):

    channel_registration_url = '/channels/food/registration'

    def setUp(self):
        super(BackendErrorTest, self).setUp()
        self.error = storage_exceptions.BackendError(ValueError())
        self.storage_error_patcher = mock.patch(
            'kinto.core.storage.memory.Storage.update',
            side_effect=self.error)

    def test_backend_errors_are_served_as_503(self):
        with self.storage_error_patcher:
            self.app.put(self.channel_registration_url,
                         headers=self.headers,
                         status=503)


class ChannelsTest(BaseWebTest, unittest.TestCase):

    channel_url = '/channels/food'
    channel_registration_url = '/channels/food/registration'

    def setUp(self):
        super(ChannelsTest, self).setUp()

    def test_channels_information_can_be_retrieved(self):
        resp = self.app.get(self.channel_url, headers=self.headers, status=200)
        assert 'data' in resp.json

        assert 'registrations' in resp.json['data']
        assert 'push' in resp.json['data']

        assert resp.json['data']['registrations'] == 0
        assert resp.json['data']['push'] == 0

    def test_registration_count_updated(self):
        self.app.put(self.channel_registration_url, headers=self.headers, status=202)
        resp = self.app.get(self.channel_url, headers=self.headers, status=200)
        assert resp.json['data']['registrations'] == 1

    def test_push_notifications_can_be_sent_to_channel_even_without_registration(self):
        self.app.post(self.channel_url, headers=self.headers, status=202)

    def test_401_without_headers(self):
        self.app.put(self.channel_registration_url, status=401)


class ChannelsNotificationTest(BaseWebTest, unittest.TestCase):

    channel_url = '/channels/food'
    channel_registration_url = '/channels/food/registration'

    def setUp(self):
        super(ChannelsNotificationTest, self).setUp()
        self.app.put(self.channel_registration_url, headers=self.headers, status=202)

    def test_push_notifications_can_be_sent_to_channel_with_registration(self):
        self.app.post(self.channel_url, headers=self.headers, status=202)
