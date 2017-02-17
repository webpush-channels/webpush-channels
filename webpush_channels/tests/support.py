from kinto.core import testing
from webpush_channels import main as webpush_main
from webpush_channels import DEFAULT_SETTINGS

P256DH = "BEVoH6cOlNPuvYR0aVJo4GVv84nbymzpXxNff7hpKYjVIFcuIEtqiLtIe4rLOXF_A2w3KWRJoCYJEjUedrXcNpc"

MINIMALIST_SUBSCRIPTION = {
    "data": {
        "endpoint": "https://updates.push.services.mozilla.com/wpush/v1/gAAAAABYZNoTAeA9vv-_zHx79",
        "keys": {
            "auth": "pnipzxpMvKBNYZAcxc-MAA",
            "p256dh": P256DH
        }
    }
}

MINIMALIST_PAYLOAD = {
    'data': {
        'url': "https://push.mozilla.com",
        'author': {
            'name': 'foobar'
        }
    }
}


class BaseWebTest(testing.BaseWebTest):

    api_prefix = "v0"
    entry_point = webpush_main

    def __init__(self, *args, **kwargs):
        super(BaseWebTest, self).__init__(*args, **kwargs)
        self.headers.update(testing.get_user_headers('mkaur'))

    def get_app_settings(self, extras=None):
        settings = DEFAULT_SETTINGS.copy()
        if extras is not None:
            settings.update(extras)
        settings = super(BaseWebTest, self).get_app_settings(extras=settings)
        return settings
