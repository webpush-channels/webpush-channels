from webpush_channels.views.subscriptions import SubscriptionSchema
import unittest


class SubscriptionSchemaTest(unittest.TestCase):
    def setUp(self):
        self.schema = SubscriptionSchema()
        self.schema = self.schema.bind()
        keys = dict(auth="authToken",
                    p256dh="encryptionKey")
        self.record = dict(endpoint="https://push.mozilla.com",
                           keys=keys)
        self.deserialized = self.schema.deserialize(self.record)

    def test_record_validation(self):
        self.assertEqual(self.deserialized, self.record)
