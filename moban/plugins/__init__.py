from moban import constants
from lml.loader import scan_plugins_regex
from moban.plugins.template import MobanFactory

BUILTIN_EXENSIONS = [
    "moban.jinja2.engine",
    "moban.data_loaders.yaml",
    "moban.data_loaders.json_loader",
    "moban.copy",
]


ENGINES = MobanFactory()


def make_sure_all_pkg_are_loaded():
    scan_plugins_regex(constants.MOBAN_ALL, "moban", None, BUILTIN_EXENSIONS)
