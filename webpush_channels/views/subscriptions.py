import colander
import hashlib
import json

from pyramid.httpexceptions import HTTPBadRequest
from pywebpush import WebPusher, WebPushException

from kinto.core.errors import http_error, ERRORS
from kinto.core.resource import register, UserResource
from kinto.core.resource.schema import ResourceSchema
from kinto.core.storage import generators


class KeySchema(colander.MappingSchema):
    auth = colander.SchemaNode(colander.String())
    p256dh = colander.SchemaNode(colander.String())


class SubscriptionSchema(ResourceSchema):
    endpoint = colander.SchemaNode(colander.String(), validator=colander.url)
    keys = KeySchema()


class SHAendpoint(generators.Generator):

    regexp = r'^[a-zA-Z0-9][a-zA-Z0-9_-]*$'

    def __init__(self, request, config=None):
        self.config = config
        self._regexp = None
        self.request = request.request

        if not self.match(self()):
            error_msg = "Generated record id does comply with regexp."
            raise ValueError(error_msg)

    def __call__(self):
        return hashlib.sha224(json.dumps(self.request.json['data']['endpoint'])).hexdigest()


@register(name='subscription',
          collection_path='/subscriptions',
          record_path='/subscriptions/{{id}}')
class Subscription(UserResource):
    schema = SubscriptionSchema

    def __init__(self, request, context=None):
        super(Subscription, self).__init__(request, context)
        if 'id' not in self.request.json['data']:
            self.model.id_generator = SHAendpoint(self, self.request)

    def process_record(self, new, old=None):
        new = super(Subscription, self).process_record(new, old)
        try:
            WebPusher(new)
        except WebPushException as e:
            raise http_error(HTTPBadRequest(),
                             errno=ERRORS.INVALID_PARAMETERS,
                             message='Invalid subscription: %s' % e)
        return new
