import colander
from kinto.core.resource import register, UserResource
from kinto.core.resource.schema import ResourceSchema


class ChannelRegistrationSchema(colander.MappingSchema):
    channel_id = colander.SchemaNode(colander.String())
    user_id = colander.SchemaNode(colander.String())


@register(name='channel',
          collection_path='/channels/channel_id',
          record_path='/channels/channel_id/registration')
class ChannelRegistration(UserResource):
    mapping = ChannelRegistrationSchema()
