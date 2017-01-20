.. _channels:

Channels
########

Basically the idea being channels is the same as TV channels where one
broadcast a message and others can listen to it.

The idea is that people can listen to channels even if they don't
exists.

The service configuration as well as the permission backend define a
list of users that can publish on given channels.

.. _channel-registration-put:

Register to a channel
=====================

.. http:put:: /channels/(channel_id)/registration

    :synopsis: Subscribe the user to the channel

    **Requires authentication**

    **Example Request**

    .. sourcecode:: bash

        $ http PUT http://localhost:9999/v0/channels/formbuilder-collections-update/registration Authorization:"Portier dccd8ac07f3e45c9907da638e994ff98" -v

    .. sourcecode:: http

        PUT /v0/channels/formbuilder-collections-update/registration HTTP/1.1
        Accept: */*
        Accept-Encoding: gzip, deflate
        Authorization: Portier dccd8ac07f3e45c9907da638e994ff98
        Connection: keep-alive
        Host: localhost:9999
        User-Agent: HTTPie/0.9.2


  **Example Response**

  .. sourcecode:: http

        HTTP/1.1 202 Accepted
        Access-Control-Expose-Headers: Backoff, Retry-After, Alert
        Date: Thu, 18 Jun 2015 17:02:23 GMT
        Server: waitress

.. _channel-registration-delete:

Unsubscribing from a channel
============================

.. http:delete:: /channels/(channel_id)/registration

    :synopsis: Unsubscribe the user from the channel

    **Requires authentication**

    **Example Request**

    .. sourcecode:: bash

        $ http delete http://localhost:9999/v0/channels/formbuilder-collections-write/registration Authorization:"Portier dccd8ac07f3e45c9907da638e994ff98" -v

    .. sourcecode:: http

        DELETE /v0/channels/formbuilder-collections-update/registration HTTP/1.1
        Accept: */*
        Accept-Encoding: gzip, deflate
        Authorization: Portier dccd8ac07f3e45c9907da638e994ff98
        Connection: keep-alive
        Host: localhost:9999
        User-Agent: HTTPie/0.9.2


  **Example Response**

  .. sourcecode:: http

        HTTP/1.1 202 Accepted
        Access-Control-Expose-Headers: Backoff, Retry-After, Alert
        Date: Thu, 18 Jun 2015 17:02:23 GMT
        Server: waitress

.. _channel-get:

Getting channels informations
=============================

.. http:get:: /channels/(channel_id)

    :synopsis: Retrieve channel informations

    **Example Request**

    .. sourcecode:: bash

        $ http get http://localhost:9999/v0/channels/formbuilder-collection-write Authorization:"Portier dccd8ac07f3e45c9907da638e994ff98" -v

    .. sourcecode:: http

        GET /v0/channels/formbuilder-collection-write HTTP/1.1
        Accept: */*
        Accept-Encoding: gzip, deflate
        Authorization: Basic Ym9iOg==
        Connection: keep-alive
        Host: localhost:9999
        User-Agent: HTTPie/0.9.2

    **Example Response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Access-Control-Expose-Headers: Backoff, Retry-After, Alert, Last-Modified, ETag
        Content-Length: 211
        Content-Type: application/json; charset=UTF-8
        Date: Thu, 18 Jun 2015 17:29:59 GMT
        Etag: "1434648599199"
        Last-Modified: Thu, 18 Jun 2015 17:29:59 GMT
        Server: waitress

        {
            "data": {
                "id": "formbuilder-collection-write",
				"registrations": 1,
				"push": 0
            }
        }


- **registration** contains the number of users that subscribed to the
  channel.
- **push** contains the number of push that were sent to the channel.

.. _channel-post:

Broadcasting a push notification
================================

For the first version, only users configured in the service
configuration can broadcast notifications.

However in the future we aim at adding a permissions management feature to
the channel.

.. http:post:: /channels/(channel_id)

    :synopsis: Push a notification

    **Requires authentication**

    **Example Request**

    .. sourcecode:: bash

        $ http post http://localhost:9999/v0/channels/formbuilder-collections-write Authorization:"Portier dccd8ac07f3e45c9907da638e994ff98" -v

    .. sourcecode:: http

        POST /v0/channels/formbuilder-collections-update HTTP/1.1
        Accept: application/json
        Accept-Encoding: gzip, deflate
        Authorization: Basic Ym9iOg==
        Connection: keep-alive
        Content-Length: 25
        Content-Type: application/json
        Host: localhost:9999
        User-Agent: HTTPie/0.9.2

        {
          "data": {
              "last_modified": 1434647996969
          }
        }


  **Example Response**

  .. sourcecode:: http

        HTTP/1.1 202 Accepted
        Access-Control-Expose-Headers: Backoff, Retry-After, Alert
        Date: Thu, 18 Jun 2015 17:02:23 GMT
        Server: waitress

The ``data`` payload will be encrypted for each subscriptions and sent
authenticated through the endpoint.
