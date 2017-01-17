# Minimal makefile for Sphinx documentation
#
VIRTUALENV = virtualenv
VENV := $(shell echo $${VIRTUAL_ENV-.venv})
PYTHON = $(VENV)/bin/python
DOC_STAMP = $(VENV)/.doc_env_installed.stamp
INSTALL_STAMP = $(VENV)/.install.stamp
DEV_STAMP = $(VENV)/.dev_env_installed.stamp

TEMPDIR := $(shell mktemp -d)

SERVER_CONFIG = config.ini


# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = $(VENV)/bin/sphinx-build
SPHINXPROJ    = webpush-channels
SOURCEDIR     = docs/source
BUILDDIR      = docs/build

# Put it first so that "make" without argument is like "make help".
help:
    @echo "Please use 'make <target>' where <target> is one of"
    @echo "  install                     install dependencies and prepare environment"
    @echo "  install-dev                 install dependencies and everything needed to run tests"
    @echo "  build-requirements          install all requirements and freeze them in requirements.txt"
    @echo "  serve                       start the webpush_channels server on default port"
    @echo "  migrate                     run the webpush_channels migrations"
    @echo "  tests-once                  only run the tests once with the default python interpreter"
    @echo "  flake8                      run the flake8 linter"
    @echo "  tests                       run all the tests with all the supported python interpreters (same as travis)"
    @echo "  clean                       remove *.pyc files and __pycache__ directory"
    @echo "  distclean                   remove *.egg-info files and *.egg, build and dist directories"
    @echo "  maintainer-clean            remove the .tox and the .venv directories"
    @echo "  docs                        build the docs"
    @echo "Check the Makefile to know exactly what each target is doing."

.PHONY: help

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(0) is meant as a shortcut for $(SPHINXOPTS).
docs: Makefile install-docs
    @$(SPHINXBUILD) -M html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(0)

install-docs: $(DOC_STAMP)
$(DOC_STAMP): $(PYTHON) docs/requirements.txt
    $(VENV)/bin/pip install -Ur docs/requirements.txt
    touch $(DOC_STAMP)

virtualenv: $(PYTHON)
$(PYTHON):
    $(VIRTUALENV) $(VENV)

install: $(INSTALL_STAMP)
$(INSTALL_STAMP): $(PYTHON) setup.py
    $(VENV)/bin/pip install -U pip
    $(VENV)/bin/pip install -Ue .
    touch $(INSTALL_STAMP)

build-requirements:
    $(VIRTUALENV) $(TEMPDIR)
    $(TEMPDIR)/bin/pip install -U pip
    $(TEMPDIR)/bin/pip install -Ue .
    $(TEMPDIR)/bin/pip freeze > requirements.txt

install-dev: $(INSTALL_STAMP) $(DEV_STAMP)
$(DEV_STAMP): $(PYTHON) dev-requirements.txt
    $(VENV)/bin/pip install -Ur dev-requirements.txt
    touch $(DEV_STAMP)

NAME := webpush-channels
SOURCE := $(shell git config remote.origin.url | sed -e 's|git@|https://|g' | sed -e 's|github.com:|github.com/|g')
VERSION := $(shell git describe --always --tag)
COMMIT := $(shell git log --pretty=format:'%H' -n 1)
version-file:
    echo '{"name":"$(NAME)","version":"$(VERSION)","source":"$(SOURCE)","commit":"$(COMMIT)"}' > version.json

serve: install-dev $(SERVER_CONFIG) version-file
    $(VENV)/bin/pserve $(SERVER_CONFIG) --reload

tests-once: install-dev version-file
    $(VENV)/bin/py.test --cov-report term-missing --cov-fail-under 100 --cov webpush_channels

flake8: install-dev
    $(VENV)/bin/flake8 webpush_channels tests

tests: version-file
    $(VENV)/bin/tox

clean:
    find . -name '*.pyc' -delete
    find . -name '__pycache__' -type d | xargs rm -fr
    rm -fr docs/_build/

distclean: clean
    rm -fr *.egg *.egg-info/ dist/ build/

maintainer-clean: distclean
    rm -fr .venv/ .tox/
