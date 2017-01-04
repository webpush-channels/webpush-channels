##############
Authentication
##############

.. _authentication:

A word about users
==================

First of all, WebPush Channels **doesn't provide users management**.

There is no such thing as user sign-up, password modification, etc.

However, users are uniquely identified.

How is that possible?
---------------------

WebPush Channels uses the request headers to authenticate the current user.

Depending on the authentication methods enabled in configuration,
the HTTP method to authenticate requests may differ.

WebPush Channels can rely on a third-party called «`Identity provider <https://en.wikipedia.org/wiki/Identity_provider>`_»
to authenticate the request and assign a :term:`user id`.

There are many identity providers solutions in the wild. The most common are OAuth,
JWT, SAML, x509, Hawk sessions...

A policy based on *OAuth2 bearer tokens* is recommended, but not mandatory.

Multiple policies
-----------------

It is possible to enable several authentication methods.
See :ref:`configuration <configuration-authentication>`.

In the current implementation, when multiple policies are configured,
the first one in the list that succeeds is picked.

:term:`User identifiers` are prefixed with the policy name being used.

OAuth Bearer token
==================

If the configured authentication policy uses *OAuth2 bearer tokens*, authentication
shall be done using this header:

::

    Authorization: Bearer <oauth_token>


The policy will verify the provided *OAuth2 bearer token* on a remote server.

:notes:

    If the token is not valid, this will result in a |status-401| error response.

Portier
-------

In order to enable authentication with :term:`Portier`, install and
configure :github:`Kinto/kinto-portier`.

Firefox Accounts
----------------

In order to enable authentication with :term:`Firefox Accounts`, install and
configure :github:`mozilla-services/kinto-fxa`.
