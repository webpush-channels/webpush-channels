import colander
from kinto.core.resource import register, UserResource
from kinto.core.resource.schema import ResourceSchema


class KeySchema(colander.MappingSchema):
    auth = colander.SchemaNode(colander.String())
    p256dh = colander.SchemaNode(colander.String())


class DataSchema(colander.MappingSchema):
    endpoint = colander.SchemaNode(colander.String(), validator=colander.url)
    keys = KeySchema()


class SubscriptionSchema(ResourceSchema):
    data = DataSchema()


@register(name='subscription',
          collection_path='/subscriptions',
          record_path='/subscriptions/{{subscription_id}}')
class Subscription(UserResource):
    mapping = SubscriptionSchema()
