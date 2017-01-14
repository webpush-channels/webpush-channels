import colander
from kinto.core.resource import register, UserResource
from kinto.core.resource.schema import ResourceSchema

class KeySchema(colander.MappingSchema):
    auth = colander.SchemaNode(colander.String())
    p256dh = colander.SchemaNode(colander.String())

class PushSchema(colander.MappingSchema):
    endpoint = colander.SchemaNode(colander.String(), validator=colander.url)
    keys = KeySchema()

class SubscriptionSchema(ResourceSchema):
    push = PushSchema()
    triggers = colander.SchemaNode(colander.Mapping(unknown='preserve'),
                                   validator=colander.All)

@register(record_methods=('GET', 'PATCH', 'DELETE'))
class Subscription(UserResource):
    mapping = SubscriptionSchema()