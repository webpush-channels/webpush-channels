from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid import httpexceptions

from kinto.core import Service

REGISTRATION_COLLECTION_ID = 'channel_registration'

channel = Service(name='channel',
                  description='Handle channel information',
                  path='/channels/{channel_id}')


channel_registration = Service(name='channel_registration',
                               description='Handle user registration for a channel',
                               path='/channels/{channel_id}/registration')


# Channel views
@channel.get(permission=NO_PERMISSION_REQUIRED)
def retrieve_channel_information(request):
    channel_id = request.matchdict['channel_id']
    parent_id = '/channels/{}'.format(channel_id)

    registrations, count = request.registry.storage.get_all(
        collection_id=REGISTRATION_COLLECTION_ID,
        parent_id=parent_id)

    return {"data": {
        "registrations": count,
        "push": 0
    }}


# Channel Registration views
@channel_registration.put(permission=NO_PERMISSION_REQUIRED)
def add_user_registration(request):
    channel_id = request.matchdict['channel_id']
    parent_id = '/channels/{}'.format(channel_id)

    request.registry.storage.update(
        collection_id=REGISTRATION_COLLECTION_ID,
        parent_id=parent_id,
        object_id=request.prefixed_userid,
        record={})
    return httpexceptions.HTTPAccepted()


@channel_registration.delete(permission=NO_PERMISSION_REQUIRED)
def remove_user_registration(request):
    channel_id = request.matchdict['channel_id']
    parent_id = '/channels/{}'.format(channel_id)

    request.registry.storage.delete(
        collection_id=REGISTRATION_COLLECTION_ID,
        parent_id=parent_id,
        object_id=request.prefixed_userid,
        with_deleted=True)
    return httpexceptions.HTTPAccepted()
