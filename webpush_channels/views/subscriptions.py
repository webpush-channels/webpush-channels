import colander

from pyramid.httpexceptions import HTTPBadRequest
from pywebpush import WebPusher

from kinto.core.errors import http_error, ERRORS
from kinto.core.resource import register, UserResource
from kinto.core.resource.schema import ResourceSchema


class KeySchema(colander.MappingSchema):
    auth = colander.SchemaNode(colander.String())
    p256dh = colander.SchemaNode(colander.String())


class SubscriptionSchema(ResourceSchema):
    endpoint = colander.SchemaNode(colander.String(), validator=colander.url)
    keys = KeySchema()


@register(name='subscription',
          collection_path='/subscriptions',
          record_path='/subscriptions/{{id}}')
class Subscription(UserResource):
    schema = SubscriptionSchema

    def process_record(self, new, old=None):
        new = super(Subscription, self).process_record(new, old)
        try:
            WebPusher(new)
        except TypeError as e:
            raise http_error(HTTPBadRequest(),
                             errno=ERRORS.INVALID_PARAMETERS,
                             message='Invalid subscription: %s' % e)
        return new
