import json
import re
import unittest
import uuid

from copy import deepcopy

from kinto.core.utils import decode_header
from kinto.core.testing import get_user_headers

from .support import BaseWebTest


MINIMALIST_SUBSCRIPTION = {
    "data": {
        "keys": {
            "auth": "authToken",
            "p256dh": "encryptionKey"
        },
        "endpoint": "https://push.mozilla.com"
    }
}


class SubscriptionsViewTest(BaseWebTest, unittest.TestCase):

    collection_url = '/subscriptions'
    _record_url = '/subscriptions/%s'

    def setUp(self):
        super(SubscriptionsViewTest, self).setUp()
        resp = self.app.post_json(self.collection_url,
                                  MINIMALIST_SUBSCRIPTION,
                                  headers=self.headers)
        self.subscription = resp.json['data']
        self.subscription_url = self._record_url % self.subscription['id']

    def test_subscriptions_can_be_accessed_by_id(self):
        self.app.get(self.subscription_url, headers=self.headers)

    def test_unknown_subscription_raises_404(self):
        new_id = '%s' % uuid.uuid4()
        other_record = self.subscription_url.replace(self.subscription['id'],
                                                     new_id)
        response = self.app.get(other_record, headers=self.headers, status=404)
        self.assertEqual(response.json['details']['id'], new_id)
        self.assertEqual(response.json['details']['resource_name'], 'subscription')

    def test_subscriptions_can_be_added(self):
        response = self.app.get(self.subscription_url, headers=self.headers)
        record = response.json['data']
        del record['id']
        del record['last_modified']
        self.assertEquals(record, MINIMALIST_SUBSCRIPTION['data'])

    def test_subscriptions_can_be_filtered_on_any_field(self):
        self.app.post_json(self.collection_url,
                           MINIMALIST_SUBSCRIPTION,
                           headers=self.headers)
        response = self.app.get(self.collection_url + '?unknown=1',
                                headers=self.headers)
        self.assertEqual(len(response.json['data']), 0)

    def test_subscriptions_can_be_sorted_on_any_field(self):
        for i in range(3):
            record = deepcopy(MINIMALIST_SUBSCRIPTION)
            record['data']['keys']['auth'] = 'Stout %s' % i
            self.app.post_json(self.collection_url,
                               record,
                               headers=self.headers)

        response = self.app.get(self.collection_url + '?_sort=-keys.auth',
                                headers=self.headers)
        names = [i['keys']['auth'] for i in response.json['data']]
        self.assertEqual(names,
                         ['authToken', 'Stout 2', 'Stout 1', 'Stout 0'])

    def test_create_a_subscription_update_collection_timestamp(self):
        collection_resp = self.app.get(self.collection_url,
                                       headers=self.headers)
        old_timestamp = int(
            decode_header(json.loads(collection_resp.headers['ETag'])))
        self.app.post_json(self.collection_url,
                           MINIMALIST_SUBSCRIPTION,
                           headers=self.headers,
                           status=201)
        collection_resp = self.app.get(self.collection_url,
                                       headers=self.headers)
        new_timestamp = int(
            decode_header(json.loads(collection_resp.headers['ETag'])))
        assert old_timestamp < new_timestamp

    def test_create_a_subscription_without_id_generates_a_uuid(self):
        resp = self.app.post_json(self.collection_url,
                                  MINIMALIST_SUBSCRIPTION,
                                  headers=self.headers,
                                  status=201)
        regexp = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-'
                            r'[0-9a-f]{4}-[0-9a-f]{12}$')
        self.assertTrue(regexp.match(resp.json['data']['id']))

    def test_create_a_subscription_with_an_invalid_id_raises(self):
        record = {'data': dict(id='a-simple-id', **MINIMALIST_SUBSCRIPTION['data'])}
        self.app.post_json(self.collection_url,
                           record,
                           headers=self.headers,
                           status=400)

    def test_create_a_subscription_with_an_id_uses_it(self):
        new_id = '%s' % uuid.uuid4()
        record = {'data': dict(id=new_id, **MINIMALIST_SUBSCRIPTION['data'])}
        resp = self.app.post_json(self.collection_url,
                                  record,
                                  headers=self.headers,
                                  status=201)
        self.assertEqual(resp.json['data']['id'], new_id)

    def test_create_a_subscription_with_an_existing_id_returns_existing(self):
        resp = self.app.post_json(self.collection_url,
                                  MINIMALIST_SUBSCRIPTION,
                                  headers=self.headers,
                                  status=201)
        existing_id = resp.json['data']['id']
        record = deepcopy(MINIMALIST_SUBSCRIPTION)
        record['data']['id'] = existing_id
        resp = self.app.post_json(self.collection_url,
                                  record,
                                  headers=self.headers,
                                  status=200)
        self.assertNotIn('stars', resp.json['data'])

    def test_create_a_subscription_with_existing_from_someone_else_gives_201(self):
        resp = self.app.post_json(self.collection_url,
                                  MINIMALIST_SUBSCRIPTION,
                                  headers=self.headers,
                                  status=201)
        existing_id = resp.json['data']['id']
        record = deepcopy(MINIMALIST_SUBSCRIPTION)
        record['data']['id'] = existing_id
        resp = self.app.post_json(self.collection_url,
                                  record,
                                  headers=get_user_headers('tartanpion'),
                                  status=201)

    def test_update_a_subscription_update_collection_timestamp(self):
        collection_resp = self.app.get(self.collection_url,
                                       headers=self.headers)
        old_timestamp = int(
            decode_header(json.loads(collection_resp.headers['ETag'])))
        self.app.put_json(self.subscription_url,
                          MINIMALIST_SUBSCRIPTION,
                          headers=self.headers,
                          status=200)
        collection_resp = self.app.get(self.collection_url,
                                       headers=self.headers)
        new_timestamp = int(
            decode_header(json.loads(collection_resp.headers['ETag'])))
        assert old_timestamp < new_timestamp

    def test_delete_a_subscription_update_collection_timestamp(self):
        collection_resp = self.app.get(self.collection_url,
                                       headers=self.headers)
        old_timestamp = int(
            decode_header(json.loads(collection_resp.headers['ETag'])))
        self.app.delete(self.subscription_url,
                        headers=self.headers,
                        status=200)
        collection_resp = self.app.get(self.collection_url,
                                       headers=self.headers)
        new_timestamp = int(
            decode_header(json.loads(collection_resp.headers['ETag'])))
        assert old_timestamp < new_timestamp

    def test_subscriptions_should_reject_unaccepted_request_content_type(self):
        headers = self.headers.copy()
        headers['Content-Type'] = 'text/plain'
        self.app.put(self.subscription_url,
                     MINIMALIST_SUBSCRIPTION,
                     headers=headers,
                     status=415)

    def test_subscriptions_should_reject_unaccepted_client_accept(self):
        headers = self.headers.copy()
        headers['Accept'] = 'text/plain'
        self.app.get(self.subscription_url,
                     MINIMALIST_SUBSCRIPTION,
                     headers=headers,
                     status=406)

    def test_subscriptions_should_accept_client_accept(self):
        headers = self.headers.copy()
        headers['Accept'] = '*/*'
        self.app.get(self.subscription_url,
                     MINIMALIST_SUBSCRIPTION,
                     headers=headers,
                     status=200)

    def test_subscriptions_can_be_created_after_deletion(self):
        self.app.delete(self.subscription_url,
                        headers=self.headers,
                        status=200)
        headers = self.headers.copy()
        headers['If-None-Match'] = '*'
        self.app.put_json(self.subscription_url, MINIMALIST_SUBSCRIPTION,
                          headers=headers, status=201)
