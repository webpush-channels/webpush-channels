import json
import unittest
import uuid

from copy import deepcopy

from kinto.core.utils import decode_header
from kinto.core.testing import get_user_headers

from .support import BaseWebTest, MINIMALIST_SUBSCRIPTION


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
            record['data']['endpoint'] = 'http://endpoint/%s' % i
            record['data']['keys']['auth'] = 'Auths%s' % i
            self.app.post_json(self.collection_url,
                               record,
                               headers=self.headers)

        response = self.app.get(self.collection_url + '?_sort=-keys.auth',
                                headers=self.headers)
        names = [i['keys']['auth'] for i in response.json['data']]
        self.assertEqual(names,
                         ['pnipzxpMvKBNYZAcxc-MAA', 'Auths2', 'Auths1', 'Auths0'])

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

    def test_invalid_id_of_subscription_should_not_be_accepted(self):
        record = {'data': dict(id='a-simple-id', **MINIMALIST_SUBSCRIPTION['data'])}
        self.app.post_json(self.collection_url,
                           record,
                           headers=self.headers,
                           status=400)

    def test_create_a_subscription_with_an_id_does_not_uses_it(self):
        new_id = '%s' % uuid.uuid4()
        record = {'data': dict(id=new_id, **MINIMALIST_SUBSCRIPTION['data'])}
        self.app.post_json(self.collection_url,
                           record,
                           headers=self.headers,
                           status=400)

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

    def test_multiple_subscriptions_merged(self):
        resp = self.app.post_json(self.collection_url,
                                  MINIMALIST_SUBSCRIPTION,
                                  headers=self.headers,
                                  status=201)
        subscription = resp.json['data']

        # XXX: Right now Kinto.core doesn't return the correct status code
        resp = self.app.post_json(self.collection_url,
                                  MINIMALIST_SUBSCRIPTION,
                                  headers=self.headers,
                                  status=201)
        new_subscription = resp.json['data']
        del new_subscription['last_modified']
        del subscription['last_modified']
        assert new_subscription == subscription


class AllResponsesAreJSONTest(BaseWebTest, unittest.TestCase):

    subscription_url = '/subscriptions'

    def setUp(self):
        self.resp = self.app.post_json(self.subscription_url,
                                       MINIMALIST_SUBSCRIPTION,
                                       headers=self.headers,
                                       status=201)

    def test_post_request_response_is_json(self):
        assert json.loads(self.resp.body)
        assert self.resp.headers['Content-Type'] == 'application/json'

    def test_get_request_response_is_json(self):
        resp = self.app.get(self.subscription_url,
                            headers=self.headers,
                            status=200)
        assert json.loads(resp.body)
        assert resp.headers['Content-Type'] == 'application/json'

    def test_delete_request_response_is_json(self):
        resp = self.app.delete(self.subscription_url,
                               headers=self.headers,
                               status=200)
        assert json.loads(resp.body)
        assert resp.headers['Content-Type'] == 'application/json'

    def test_delete_specific_subscription_request_response_is_json(self):
        resp = self.app.delete(self.subscription_url+'/'+self.resp.json['data']['id'],
                               headers=self.headers,
                               status=200)
        assert json.loads(resp.body)
        assert resp.headers['Content-Type'] == 'application/json'

    def test_get_request_for_unknown_subscription_url_response_is_json(self):
        resp = self.app.get('/foo',
                            headers=self.headers,
                            status=404)
        assert json.loads(resp.body)
        assert resp.headers['Content-Type'] == 'application/json'

    def test_post_invalid_subscription_response_is_json(self):
        INVALID_SUBSCRIPTION = deepcopy(MINIMALIST_SUBSCRIPTION)
        INVALID_SUBSCRIPTION['keys'] = ''
        resp = self.app.post_json(self.subscription_url,
                                  INVALID_SUBSCRIPTION,
                                  headers=self.headers,
                                  status=400)
        assert json.loads(resp.body)
        assert resp.headers['Content-Type'] == 'applicatigon/json'

    def test_delete_request_for_unknown_subscription_url_response_is_json(self):
        resp = self.app.delete('/foo',
                               headers=self.headers,
                               status=404)
        assert json.loads(resp.body)
        assert resp.headers['Content-Type'] == 'application/json'

    def test_delete_nonexistent_subscription_request_response_is_json(self):
        resp = self.app.delete(self.subscription_url+'/'+'blah',
                               headers=self.headers,
                               status=404)
        assert json.loads(resp.body)
        assert resp.headers['Content-Type'] == 'application/json'
