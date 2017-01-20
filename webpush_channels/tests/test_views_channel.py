import unittest
from .support import BaseWebTest, MINIMALIST_REGISTRATION


class ChannelRegistrationTest(BaseWebTest, unittest.TestCase):
    channel_registration_url = '/channels/food/registration'

    def setUp(self):
        super(CollectionRegistrationTest, self).setUp()
        self.app.put_json(channel_registration_url, MINIMALIST_REGISTRATION,
                          headers=self.headers)
