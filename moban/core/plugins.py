from lml.loader import scan_plugins_regex

from moban import constants

BUILTIN_EXENSIONS = [
    "moban.plugins.jinja2.engine",
    "moban.plugins.yaml_loader",
    "moban.plugins.json_loader",
    "moban.plugins.copy",
    "moban.plugins.delete",
    "moban.plugins.strip",
]


def make_sure_all_pkg_are_loaded():
    scan_plugins_regex(constants.MOBAN_ALL, "moban", None, BUILTIN_EXENSIONS)
