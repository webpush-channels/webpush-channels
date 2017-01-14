import colander
from webpush_channels.views.subscriptions import SubscriptionSchema
import unittest

class SubscriptionSchemaTest(unittest.TestCase):
	def setUp(self):
		self.schema = SubscriptionSchema()
		self.schema = self.schema.bind()
		keys = dict(auth="authToken",
        			p526dh="encryptionKey")
		push = dict(endpoint="https://push.mozilla.com",
        			keys=keys)
		actions = ["write"]
		path = "/buckets/blocklists/collections/*/records"
		triggers = dict(path=actions)
		self.record = dict(push=push,
        				   triggers=triggers)
		self.deserialized = self.schema.deserialize(self.record)

	def test_record_validation(self):
		self.assertEqual(self.deserialized['push'], self.record['push'])

