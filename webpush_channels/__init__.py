import pkg_resources
import logging

from pyramid.config import Configurator
from pyramid.settings import asbool

import kinto.core


# Module version, as defined in PEP-0396.
__version__ = pkg_resources.get_distribution(__package__).version

# The API version is derivated from the module version.
API_VERSION = 'v%s' % __version__.split('.')[0]

# Main readinglist logger
logger = logging.getLogger(__name__)


DEFAULT_SETTINGS = {
    'kinto.core.paginate_by': 100
}


def main(global_config, **settings):
    config = Configurator(settings=settings)

    kinto.core.initialize(config, version=__version__,
                       default_settings=DEFAULT_SETTINGS)

    config.scan("webpush_channels.views")
    app = config.make_wsgi_app()
    return kinto.core.install_middlewares(app, settings)
