import hashlib

import colander
from pyramid.httpexceptions import HTTPBadRequest
from pywebpush import WebPusher, WebPushException

from kinto.core.errors import http_error, ERRORS
from kinto.core.resource import register, UserResource, ResourceSchema
from kinto.core.storage import generators

from ..utils import canonical_json


def generate_id(subscription):
    return hashlib.sha256(canonical_json(subscription).encode('utf-8')).hexdigest()


class KeySchema(colander.MappingSchema):
    auth = colander.SchemaNode(colander.String())
    p256dh = colander.SchemaNode(colander.String())


class SubscriptionSchema(ResourceSchema):
    id = colander.SchemaNode(colander.String(), missing=colander.drop)
    endpoint = colander.SchemaNode(colander.String(), validator=colander.url)
    keys = KeySchema()

    def deserialize(self, cstruct):
        """Preprocess received data to make sure if an id is present it has
        the correct value.

        """
        record = super(SubscriptionSchema, self).deserialize(cstruct)
        given_id = record.get('id')
        generated_id = generate_id(record['endpoint'])

        if given_id and given_id != generated_id:
            raise colander.Invalid(
                self, msg="Invalid ID: '{}' found while it should be '{}'".format(
                    given_id, generated_id))

        return super(SubscriptionSchema, self).deserialize(cstruct)


class SHA256Generator(generators.Generator):

    regexp = r'^[a-zA-Z0-9][a-zA-Z0-9_-]*$'

    def __init__(self, request, config=None):
        self.request = request
        super(SHA256Generator, self).__init__(config)

    def __call__(self):
        if 'body' not in self.request.validated:
            return generate_id(None)

        body = self.request.validated['body']['data']
        return generate_id(body['endpoint'])


@register(name='subscription',
          collection_path='/subscriptions',
          record_path='/subscriptions/{{id}}')
class Subscription(UserResource):
    schema = SubscriptionSchema
    preserve_unknown = False

    def __init__(self, request, *args, **kwargs):
        super(Subscription, self).__init__(request, *args, **kwargs)
        self.model.id_generator = SHA256Generator(request)

    def process_record(self, new, old=None):
        new = super(Subscription, self).process_record(new, old)
        try:
            WebPusher(new)
        except WebPushException as e:
            raise http_error(HTTPBadRequest(),
                             errno=ERRORS.INVALID_PARAMETERS,
                             message='Invalid subscription: %s' % e)
        return new
