from webpush_channels.views.channels import ChannelRegistrationSchema
import unittest


class ChannelRegistrationSchemaTest(unittest.TestCase):
    def setUp(self):
        self.schema = ChannelRegistrationSchema()
        self.schema = self.schema.bind()
        self.record = dict(channel_id="channel_name",
                           user_id="portier:mkaur@mozilla.com")
        self.deserialized = self.schema.deserialize(self.record)

    def test_record_validation(self):
        self.assertEqual(self.deserialized, self.record)
