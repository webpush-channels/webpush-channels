import unittest

from webpush_channels.views.channels import PayloadSchema

from .support import MINIMALIST_PAYLOAD


class PayloadSchemaTest(unittest.TestCase):
    def setUp(self):
        self.schema = PayloadSchema()
        self.schema = self.schema.bind()

    def test_record_validation(self):
        deserialized = self.schema.deserialize(MINIMALIST_PAYLOAD)
        self.assertEqual(deserialized, MINIMALIST_PAYLOAD)

    def test_empty_record_validation(self):
        deserialized = self.schema.deserialize({})
        self.assertEqual(deserialized, {})
