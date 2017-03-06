.. _tutorial-first-steps:

First steps with webpush-channels API
#####################################

This tutorial will take you through your first API calls with a real
webpush-channels server.

In order to get the most out of this tutorial, you may want to have a
real webpush-channels server ready. You can read our :ref:`installation
<install>` guide to see how to set up your own webpush-channels instance if you
like. We'll be using the :ref:`Mozilla demo server <run-webpush-channels-mozilla-demo>`.

.. important::

    In this tutorial we will use a Basic Authentication, which computes a
    user id based on the token provided in the request.

    This method has many limitations but has the advantage of not needing
    specific setup or third-party services before you get started.

    :ref:`Read more about authentication in webpush-channels <authentication>`.

subscription and channel APIs
=============================

Using the `httpie <http://httpie.org>`_ tool we can post a sample subscription:

.. note::

    Please `consider reading httpie documentation <https://github.com/jkbrzt/httpie#proxies>`_
    for more information (if you need to configure a proxy, for instance).

.. code-block:: shell

    $ echo '{"data": {"endpoint": "https://updates.push.services.mozilla.com/wpush/v1/gAAAAABYZNChoTLTAeA9vv-_zeqGuZiM4ESpiV7oiT5XtrN8aI01fiCQ7-_hC8lhqXanjUEWp5MFRoq35QmzdplCkRhp5nRgjwneGCGO8WXYH9psZaD_xInKLWm7K8-tzFAp-vRNHx79","keys": {"auth": "pnipzxpMvKBNYZAcxc-MAA","p256dh": "BEVoH6cOlNPuvYR0aVJo4GVv84nbymzpXxNff7hpKYjVIFcuIEtqiLtIe4rLOXF_A2w3KWRJoCYJEjUedrXcNpc"}}}' | http POST https://webpush-channels.dev.mozaws.net/v0/subscriptions -v --auth 'token:my-secret'

.. code-block:: http

    HTTP/1.1 201 Created
    Access-Control-Expose-Headers: Retry-After, Backoff, Content-Length, Alert
    Connection: keep-alive
    Content-Length: 457
    Content-Type: application/json
    Date: Mon, 06 Mar 2017 08:46:54 GMT
    ETag: "1488790014966"
    Last-Modified: Mon, 06 Mar 2017 08:46:54 GMT
    Server: nginx
    X-Content-Type-Options: nosniff

    {
        "data": {
            "endpoint": "https://updates.push.services.mozilla.com/wpush/v1/gAAAAABYZNChoTLTAeA9vv-_zeqGuZiM4ESpiV7oiT5XtrN8aI01fiCQ7-_hC8lhqXanjUEWp5MFRoq35QmzdplCkRhp5nRgjwneGCGO8WXYH9psZaD_xInKLWm7K8-tzFAp-vRNHx79",
            "id": "2bc46e881676cd7321d12e9e2deb5c46e3ad8ccabaf580df3fc104fc46e114e1",
            "keys": {
                "auth": "pnipzxpMvKBNYZAcxc-MAA",
                "p256dh": "BEVoH6cOlNPuvYR0aVJo4GVv84nbymzpXxNff7hpKYjVIFcuIEtqiLtIe4rLOXF_A2w3KWRJoCYJEjUedrXcNpc"
            },
            "last_modified": 1488790014966
        }
    }


.. note::

    With *Basic Auth* a unique identifier needs to be associated with each
    user. This identifier is built using the token value provided in the request.
    Therefore users cannot change their password easily without losing
    access to their data. :ref:`More information <authentication>`.

Let us register for a channel named 'blah' now:

.. code-block:: shell

    $ http PUT https://webpush-channels.dev.mozaws.net/v0/channels/blah/registration \
           -v --auth 'token:my-secret'

.. code-block:: http

    HTTP/1.1 202 Accepted
    Access-Control-Expose-Headers: Retry-After, Backoff, Content-Length, Alert
    Connection: keep-alive
    Content-Length: 33
    Content-Type: application/json
    Date: Mon, 06 Mar 2017 08:50:52 GMT
    Server: nginx
    X-Content-Type-Options: nosniff

    {
        "code": 202,
        "message": "Accepted"
    }

To be able to post messages to a channel:

.. code-block:: shell

    $ http POST https://webpush-channels.dev.mozaws.net/v0/channels/blah \
           -v --auth 'token:my-secret'

.. code-block:: http

    HTTP/1.1 202 Accepted
    Access-Control-Expose-Headers: Retry-After, Backoff, Content-Length, Alert
    Connection: keep-alive
    Content-Length: 33
    Content-Type: application/json
    Date: Mon, 06 Mar 2017 08:58:50 GMT
    Server: nginx
    X-Content-Type-Options: nosniff

    {
        "code": 202,
        "message": "Accepted"
    }

Conclusion
==========

In this tutorial you have seen some of the concepts exposed by *webpush-channels*:

- Subscribing for push notifications
- Registering for a channel
- Pushing a message through mozilla push server

.. note::

    We are working to improve our documentation and make sure it is as easy as
    possible to get started with *webpush-channels*.
