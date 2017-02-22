import unittest
from copy import deepcopy
import json

import mock

from kinto.core import testing
from kinto.core.storage import exceptions as storage_exceptions

from ..utils import canonical_json
from .support import BaseWebTest, MINIMALIST_SUBSCRIPTION, MINIMALIST_PAYLOAD


class ChannelRegistrationTest(BaseWebTest, unittest.TestCase):

    channel_url = '/channels/food'
    channel_registration_url = '/channels/food/registration'

    def setUp(self):
        super(ChannelRegistrationTest, self).setUp()
        self.error = storage_exceptions.BackendError(ValueError())

    def test_registration_can_be_added_for_a_user(self):
        self.app.put(self.channel_registration_url, headers=self.headers, status=202)
        resp = self.app.get(self.channel_url, headers=self.headers, status=200)
        assert resp.json['data']['registrations'] == 1

    def test_remove_non_existent_registration(self):
        self.app.delete(self.channel_registration_url, headers=self.headers, status=202)

    def test_we_cannot_register_an_anonymous_user(self):
        self.app.put(self.channel_registration_url, status=401)

    def test_we_cannot_unregister_an_anonymous_user(self):
        self.app.delete(self.channel_registration_url, status=401)

    def test_backend_errors_are_served_as_503_on_registration(self):
        with mock.patch('kinto.core.storage.memory.Storage.update', side_effect=self.error):
            self.app.put(self.channel_registration_url,
                         headers=self.headers,
                         status=503)

    def test_backend_errors_are_served_as_503_on_channel(self):
        with mock.patch('kinto.core.storage.memory.Storage.get_all', side_effect=self.error):
            self.app.get(self.channel_url,
                         headers=self.headers,
                         status=503)


class EmptyChannelsTest(BaseWebTest, unittest.TestCase):

    channel_url = '/channels/food'
    channel_registration_url = '/channels/food/registration'

    def test_push_notifications_can_be_sent_to_channel_even_without_anyone_being_registered(self):
        self.app.post(self.channel_url, headers=self.headers, status=202)

    def test_we_cannot_access_the_channel_information_anonymously(self):
        self.app.get(self.channel_url, status=401)

    def test_we_cannot_access_the_channel_information_if_we_are_not_registered(self):
        self.app.get(self.channel_url, headers=self.headers, status=403)


class RegisteredChannelsTest(BaseWebTest, unittest.TestCase):

    channel_url = '/channels/food'
    channel_registration_url = '/channels/food/registration'
    subscription_url = '/subscriptions'

    def setUp(self):
        super(RegisteredChannelsTest, self).setUp()
        self.app.put(self.channel_registration_url, headers=self.headers, status=202)

    def test_channels_information_can_be_retrieved(self):
        resp = self.app.get(self.channel_url, headers=self.headers, status=200)
        assert 'data' in resp.json

        assert 'registrations' in resp.json['data']
        assert 'push' in resp.json['data']

        assert resp.json['data']['registrations'] == 1
        assert resp.json['data']['push'] == 0

    def test_registration_count_updated(self):
        headers = self.headers.copy()
        headers.update(testing.get_user_headers('natim'))
        self.app.put(self.channel_registration_url, headers=headers, status=202)
        resp = self.app.get(self.channel_url, headers=self.headers, status=200)
        assert resp.json['data']['registrations'] == 2

    def test_registration_can_be_remove_for_a_user(self):
        headers = self.headers.copy()
        headers.update(testing.get_user_headers('natim'))
        self.app.put(self.channel_registration_url, headers=headers, status=202)
        self.app.delete(self.channel_registration_url, headers=headers, status=202)
        resp = self.app.get(self.channel_url, headers=self.headers, status=200)
        assert resp.json['data']['registrations'] == 1

    def test_push_notifications_can_be_sent_to_channel_with_registration_but_no_subscription(self):
        self.app.post(self.channel_url, headers=self.headers, status=202)


class RegisteredAndSubscribedChannelsTest(BaseWebTest, unittest.TestCase):
    channel_url = '/channels/food'
    channel_registration_url = '/channels/food/registration'
    subscription_url = '/subscriptions'

    def setUp(self):
        super(RegisteredAndSubscribedChannelsTest, self).setUp()
        self.app.put(self.channel_registration_url, headers=self.headers, status=202)
        resp = self.app.post_json(self.subscription_url,
                                  MINIMALIST_SUBSCRIPTION,
                                  headers=self.headers)
        self.subscription = resp.json['data']
        del self.subscription['id']
        del self.subscription['last_modified']
        self.subscription['keys']['auth'] = self.subscription['keys']['auth'].encode('utf-8')
        self.subscription['keys']['p256dh'] = self.subscription['keys']['p256dh'].encode('utf-8')

        self.webpusher_error_patcher = mock.patch('webpush_channels.views.channels.WebPusher')

    def test_push_notifications_can_be_sent_with_no_payload(self):
        with self.webpusher_error_patcher as webpusher_mock:
            self.app.post(self.channel_url, headers=self.headers, status=202)
            webpusher_mock.assert_called_with(self.subscription)
            webpusher_mock.return_value.send.assert_called_with(data=None, ttl=15)

    def test_push_notification_can_take_a_payload(self):
        with self.webpusher_error_patcher as webpusher_mock:
            self.app.post_json(self.channel_url, MINIMALIST_PAYLOAD,
                               headers=self.headers, status=202)
            webpusher_mock.assert_called_with(self.subscription)
            webpusher_mock.return_value.send.assert_called_with(
                data=canonical_json(MINIMALIST_PAYLOAD['data']), ttl=15)

    def test_invalid_encryption_keys_shows_error(self):
        CHANGED_SUBSCRIPTION = deepcopy(MINIMALIST_SUBSCRIPTION)
        CHANGED_SUBSCRIPTION['data']['keys']['p256dh'] = 'yAB'

        self.app.post_json(self.subscription_url,
                           CHANGED_SUBSCRIPTION,
                           headers=self.headers, status=400)


class AllResponsesAreJSONTest(BaseWebTest, unittest.TestCase):

    channel_url = '/channels/food'
    channel_registration_url = '/channels/food/registration'
    subscription_url = '/subscriptions'

    def setUp(self):
        super(AllResponsesAreJSONTest, self).setUp()
        self.app.post_json(self.subscription_url,
                           MINIMALIST_SUBSCRIPTION,
                           headers=self.headers)
        self.resp = self.app.put(self.channel_registration_url, headers=self.headers, status=202)

    def test_put_request_response_is_json(self):
        assert self.resp.json == {}
        assert self.resp.headers['Content-Type'] == 'application/json'

    def test_delete_request_response_is_json(self):
        resp = self.app.delete(self.channel_registration_url, headers=self.headers, status=202)
        assert resp.json == {}
        assert resp.headers['Content-Type'] == 'application/json'

    def test_get_request_response_is_json(self):
        resp = self.app.get(self.channel_url, headers=self.headers, status=200)
        assert json.loads(resp.body)
        assert resp.headers['Content-Type'] == 'application/json'

    def test_post_request_response_is_json(self):
        resp = self.app.post(self.channel_url, headers=self.headers, status=202)
        assert resp.json == {}
        assert resp.headers['Content-Type'] == 'application/json'
