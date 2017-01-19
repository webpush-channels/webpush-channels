.. _api-endpoints:

1.x
###

Full reference
==============

Full detailed API documentation:

.. toctree::
   :maxdepth: 1

   authentication
   channels
   subscriptions
   utilities
   backoff
   errors
   deprecation


Cheatsheet
==========

+----------+------------------------------------------------------------------------------+-----------------------------------------------------------------+
| Method   | URI                                                                          | Description                                                     |
+==========+==============================================================================+=================================================================+
| `GET`    | :ref:`/ <api-utilities>`                                                     | :ref:`Information about the running instance                    |
|          |                                                                              | <api-utilities>`                                                |
+----------+------------------------------------------------------------------------------+-----------------------------------------------------------------+
| `GET`    | :ref:`/__heartbeat__ <api-utilities>`                                        | :ref:`Return the status of dependent services                   |
|          |                                                                              | <api-utilities>`                                                |
+----------+------------------------------------------------------------------------------+-----------------------------------------------------------------+

| **Channels**
                                                    |

+----------+------------------------------------------------------------------------+-----------------------------------------------------------------+

| `PUT`    | :ref:`/channels/(channel_id)/registration <channel-registration-put>`  | :ref:`Subscribe to a channel <channel-registration-put>`	     |

+----------+---------------------------------------------------------------------------+-------------------------------------------------------------------+

| `DELETE` | :ref:`/channels/(channel_id)/registration <channel-registration-delete>`  | :ref:`Unsubscribe from a channel <channel-registration-delete>`  |

+----------+----------------------------------------------+-----------------------------------------------------------------+

| `GET`    | :ref:`/channels/(channel_id) <channel-get>`  | :ref:`Get channel details <channel-get>`
                |

+----------+-----------------------------------------------+-----------------------------------------------------------------+

| `POST`   | :ref:`/channels/(channel_id) <channel-post>`  | :ref:`Broadcast push notification <channel-post>`               |

+----------+------------------------------------------------------------------------------+-----------------------------------------------------------------+

| **Subscriptions**                                                                                                                                         |

+----------+------------------------------------------------------------------------------+-----------------------------------------------------------------+

| `POST`   | :ref:`/subscriptions <subscriptions-post>`                                   | :ref:`Add a new user subscription <subscriptions-post>`         |

+----------+------------------------------------------------------------------------------+-----------------------------------------------------------------+

| `GET`    | :ref:`/subscriptions <subscriptions-get>`                                    | :ref:`Get the list of user's subscriptions <subscriptions-get>`
													|

+----------+---------------------------------------------------+-----------------------------------------------------------------+

| `DELETE` | :ref:`/subscriptions <subscriptions-delete>`      | :ref:`Delete user's subscriptions <subscriptions-delete>`   |

+----------+----------------------------------------------------------------+-----------------------------------------------------------------+

| `DELETE` | :ref:`/subscriptions/(subscription_id) <subscription-delete>`  | :ref:`Delete an user subscription <subscription-delete>`   |

+----------+------------------------------------------------------------------------------+-----------------------------------------------------------------+
