import colander
from kinto.core.resource import register, UserResource
from kinto.core.resource.schema import ResourceSchema
from pyramid.httpexceptions import HTTPNotFound
from kinto.core.events import ACTIONS


class ChannelRegistrationSchema(ResourceSchema):
    channel_id = colander.SchemaNode(colander.String())
    user_id = colander.SchemaNode(colander.String())


@register(name='channel',
          collection_path='/channels/{{channel_id}}/registration',
          record_path='/channels/{{channel_id}}/registration/{{id}}',
          collection_methods=('PUT', 'DELETE'))
class ChannelRegistration(UserResource):
    mapping = ChannelRegistrationSchema()

    def collection_put(self):
        new_record = self.request.validated['body'].get('data', {})
        try:
            id_field = self.model.id_field
            new_record[id_field] = _id = self.request.json['data'][id_field]
            self._raise_400_if_invalid_id(_id)
            existing = self._get_record_or_404(_id)
        except (HTTPNotFound, KeyError, ValueError):
            existing = None

        self._raise_412_if_modified(record=existing)

        if existing:
            new_record = self.process_record(new_record)
            record = self.model.update_record(new_record)
            action = ACTIONS.UPDATE
        else:
            new_record = self.process_record(new_record)
            record = self.model.create_record(new_record)
            self.request.response.status_code = 201
            action = ACTIONS.CREATE

        timestamp = record[self.model.modified_field]
        self._add_timestamp_header(self.request.response, timestamp=timestamp)

        return self.postprocess(record, action=action)
