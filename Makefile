# Minimal makefile for Sphinx documentation
#
VIRTUALENV = virtualenv
VENV := $(shell echo $${VIRTUAL_ENV-.venv})
PYTHON = $(VENV)/bin/python
DOC_STAMP = $(VENV)/.doc_env_installed.stamp

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = $(VENV)/bin/sphinx-build
SPHINXPROJ    = webpush-channels
SOURCEDIR     = docs/source
BUILDDIR      = docs/build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
html: Makefile install-docs
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

install-docs: $(DOC_STAMP)
$(DOC_STAMP): $(PYTHON) docs/requirements.txt
	$(VENV)/bin/pip install -Ur docs/requirements.txt
	touch $(DOC_STAMP)

virtualenv: $(PYTHON)
$(PYTHON):
	$(VIRTUALENV) $(VENV)
