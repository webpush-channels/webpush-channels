.. _run-webpush-channels-mozilla-demo:

Mozilla demo server
===================

A webpush-channels instance is running at https://webpush-channels.dev.mozaws.net/v0/

.. _run-webpush-channels-python:

Using the Python package
========================

System requirements
-------------------

Depending on the platform and chosen configuration, some libraries or
extra services are required.

The following commands will install necessary tools for cryptography
and Python packaging like `Virtualenv <https://virtualenv.pypa.io/>`_.

Linux
'''''

On Debian / Ubuntu based systems::

    apt-get install libffi-dev libssl-dev python-dev python-virtualenv

On RHEL-derivatives::

    dnf install libffi-devel openssl-devel python-devel python-virtualenv

OS X
''''

Assuming `brew <http://brew.sh/>`_ is installed:

::

    brew install libffi openssl pkg-config python

    pip install virtualenv


Quick start
-----------

By default, for convenience, *webpush-channels* persists the subscriptions and channel
registartions in a **volatile** memory backend. On every restart, the server
will lose its data, and multiple processes are not handled properly.

But it should be enough to get started!


Create a Python isolated environment:

::

    virtualenv env/
    source env/bin/activate

Install kinto:

::

    pip install kinto

Then install the package using the default configuration:

::

    pip install --upgrade pip
    pip install webpush-channels

::

    kinto --ini config.ini migrate

The server should now be running on http://localhost:9999


.. _run-webpush-channels-from-source:

From sources
============

If you plan on contributing, this is the way to go!

This will install every necessary packages to run the tests, build the
documentation etc.

Make sure you have the system requirements listed in the
:ref:`Python package <run-webpush-channels-python>` section.
Also, make sure you have kinto installed.
If not, follow this:

::
    pip install kinto

Get the source code:

::

    git clone https://github.com/webpush-channels/webpush-channels.git
    cd webpush-channels/
    make serve

The server should now be running with the default configuration on http://localhost:9999
