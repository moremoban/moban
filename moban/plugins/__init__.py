from lml.loader import scan_plugins_regex
from moban.plugins.template import TemplateFactory
from moban import constants


BUILTIN_EXENSIONS = [
    "moban.jinja2.engine",
    "moban.data_loaders.yaml",
    "moban.data_loaders.json_loader",
    "moban.copy",
]


ENGINES = TemplateFactory()


def make_sure_all_pkg_are_loaded():
    scan_plugins_regex(constants.MOBAN_ALL, "moban", None, BUILTIN_EXENSIONS)
