.. _subscriptions:

Subscriptions
#############

Subscriptions belongs to an user.

A user can have multiple subscriptions (one per browser session or
device).

A subscription consist on the information that you can get from a
requesting a Push subscription on the browser.

.. code-block:: json

    {
    	"data": {
            "endpoint": "https://updates.push.services.mozilla.com/wpush/v1/gAAAAABYZNChoTLTAeA9vv-_zeqGuZiM4ESpiV7oiT5XtrN8aI01fiCQ7-_hC8lhqXanjUEWp5MFRoq35QmzdplCkRhp5nRgjwneGCGO8WXYH9psZaD_xInKLWm7K8-tzFAp-vRNHx79",
            "keys": {
                "auth": "pnipzxpMvKBNYZAcxc-MAA",
                "p256dh": "BEVoH6cOlNPuvYR0aVJo4GVv84nbymzpXxNff7hpKYjVIFcuIEtqiLtIe4rLOXF_A2w3KWRJoCYJEjUedrXcNpc"
            }
        }
    }



.. _subscriptions-post:

Add a new user subscription
===========================

.. http:post:: /subscriptions

    :synopsis: Store a subscription. The ID will be assigned automatically.


    **Requires authentication**

    **Example Request**

    .. sourcecode:: bash

        $ echo '{"data": {"endpoint": "URL", "keys": {}}}' | http post http://localhost:9999/v0/subscriptions Authorization:"Portier dccd8ac07f3e45c9907da638e994ff98" -v

    .. sourcecode:: http

        POST /v0/subscriptions HTTP/1.1
        Accept: application/json
        Accept-Encoding: gzip, deflate
        Authorization: Portier dccd8ac07f3e45c9907da638e994ff98
        Connection: keep-alive
        Content-Length: 25
        Content-Type: application/json
        Host: localhost:9999
        User-Agent: HTTPie/0.9.2

        {
        	"data": {
                "endpoint": "https://updates.push.services.mozilla.com/wpush/v1/gAAAAABYZNChoTLTAeA9vv-_zeqGuZiM4ESpiV7oiT5XtrN8aI01fiCQ7-_hC8lhqXanjUEWp5MFRoq35QmzdplCkRhp5nRgjwneGCGO8WXYH9psZaD_xInKLWm7K8-tzFAp-vRNHx79",
                "keys": {
                    "auth": "pnipzxpMvKBNYZAcxc-MAA",
                    "p256dh": "BEVoH6cOlNPuvYR0aVJo4GVv84nbymzpXxNff7hpKYjVIFcuIEtqiLtIe4rLOXF_A2w3KWRJoCYJEjUedrXcNpc"
                }
            }
        }

  **Example Response**

  .. sourcecode:: http

        HTTP/1.1 201 Created
        Access-Control-Expose-Headers: Backoff, Retry-After, Alert
        Content-Length: 199
        Content-Type: application/json; charset=UTF-8
        Date: Thu, 18 Jun 2015 17:02:23 GMT
        Server: waitress

        {
        	"data": {
                "endpoint": "https://updates.push.services.mozilla.com/wpush/v1/gAAAAABYZNChoTLTAeA9vv-_zeqGuZiM4ESpiV7oiT5XtrN8aI01fiCQ7-_hC8lhqXanjUEWp5MFRoq35QmzdplCkRhp5nRgjwneGCGO8WXYH9psZaD_xInKLWm7K8-tzFAp-vRNHx79",
                "keys": {
                    "auth": "pnipzxpMvKBNYZAcxc-MAA",
                    "p256dh": "BEVoH6cOlNPuvYR0aVJo4GVv84nbymzpXxNff7hpKYjVIFcuIEtqiLtIe4rLOXF_A2w3KWRJoCYJEjUedrXcNpc"
                }
            }
        }

.. include:: _details-post-list.rst

.. include:: _status-post-list.rst


.. _subscriptions-get:

Retrieving user's subscriptions
===============================

.. http:get:: /subscriptions

    :synopsis: Retrieve all the subscriptions for the user.

    **Requires authentication**

    **Example Request**

    .. sourcecode:: bash

        $ http get http://localhost:9999/v0/subscriptions Authorization:"Portier dccd8ac07f3e45c9907da638e994ff98"

    .. sourcecode:: http

        GET /v0/subscriptions HTTP/1.1
        Accept: */*
        Accept-Encoding: gzip, deflate
        Authorization: Portier dccd8ac07f3e45c9907da638e994ff98
        Connection: keep-alive
        Host: localhost:9999
        User-Agent: HTTPie/0.9.2

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Access-Control-Expose-Headers: Backoff, Retry-After, Alert, Next-Page, Total-Records, Last-Modified, ETag
        Content-Length: 110
        Content-Type: application/json; charset=UTF-8
        Date: Thu, 18 Jun 2015 17:24:38 GMT
        Etag: "1434648278603"
        Last-Modified: Thu, 18 Jun 2015 17:24:38 GMT
        Server: waitress
        Total-Records: 1

        {
            "data": [
			    {
                    "endpoint": "https://updates.push.services.mozilla.com/wpush/v1/gAAAAABYZNChoTLTAeA9vv-_zeqGuZiM4ESpiV7oiT5XtrN8aI01fiCQ7-_hC8lhqXanjUEWp5MFRoq35QmzdplCkRhp5nRgjwneGCGO8WXYH9psZaD_xInKLWm7K8-tzFAp-vRNHx79",
                    "keys": {
                        "auth": "pnipzxpMvKBNYZAcxc-MAA",
                        "p256dh": "BEVoH6cOlNPuvYR0aVJo4GVv84nbymzpXxNff7hpKYjVIFcuIEtqiLtIe4rLOXF_A2w3KWRJoCYJEjUedrXcNpc"
                    },
                    "id": "89881454-e4e9-4ef0-99a9-404d95900352",
                    "last_modified": 1434647996969
                }
            ]
        }


.. _subscriptions-delete:

Delete user's subscriptions
===========================

.. http:delete:: /subscriptions

    :synopsis: Delete all the user's subscriptions

    **Requires authentication**

    **Example Request**

    .. sourcecode:: bash

        $ http delete http://localhost:9999/v0/subscriptions Authorization:"Portier dccd8ac07f3e45c9907da638e994ff98"

    .. sourcecode:: http

        DELETE /v0/subscriptions HTTP/1.1
        Accept: */*
        Accept-Encoding: gzip, deflate
        Authorization: Portier dccd8ac07f3e45c9907da638e994ff98
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
            "data": [{
                "deleted": true,
                "id": "89881454-e4e9-4ef0-99a9-404d95900352",
                "last_modified": 1434648749173
            }]
        }


.. _subscription-delete:

Deleting a single subscription
==============================

.. http:delete:: /subscriptions/(subscription_id)

    :synopsis: Delete a subscription by its ID.

    **Example Request**

    .. sourcecode:: bash

        $ http delete http://localhost:9999/v0/subscriptions/89881454-e4e9-4ef0-99a9-404d95900352  Authorization:"Portier dccd8ac07f3e45c9907da638e994ff98"

    .. sourcecode:: http

        DELETE /v0/subscriptions/89881454-e4e9-4ef0-99a9-404d95900352 HTTP/1.1
        Accept: */*
        Accept-Encoding: gzip, deflate
        Authorization: Portier dccd8ac07f3e45c9907da638e994ff98
        Connection: keep-alive
        Content-Length: 0
        Host: localhost:9999
        User-Agent: HTTPie/0.9.2

    **Example Response**

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Access-Control-Expose-Headers: Backoff, Retry-After, Alert
        Content-Length: 99
        Content-Type: application/json; charset=UTF-8
        Date: Thu, 18 Jun 2015 17:32:29 GMT
        Server: waitress

        {
            "data": {
                "deleted": true,
                "id": "89881454-e4e9-4ef0-99a9-404d95900352",
                "last_modified": 1434648749173
            }
        }
