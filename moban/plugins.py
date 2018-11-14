import os

from lml.loader import scan_plugins_regex
from lml.plugin import PluginManager

from moban import utils, constants, exceptions
from moban.constants import MOBAN_ALL
from moban.jinja2.extensions import (
    JinjaTestManager,
    JinjaFilterManager,
    JinjaGlobalsManager,
)

FILTERS = JinjaFilterManager()
TESTS = JinjaTestManager()
GLOBALS = JinjaGlobalsManager()

BUILTIN_EXENSIONS = [
    "moban.jinja2.filters.repr",
    "moban.jinja2.filters.github",
    "moban.jinja2.filters.text",
    "moban.jinja2.tests.files",
]


def refresh_plugins():
    scan_plugins_regex(MOBAN_ALL, "moban", None, BUILTIN_EXENSIONS)


class LibraryManager(PluginManager):
    def __init__(self):
        super(LibraryManager, self).__init__(constants.LIBRARY_EXTENSION)

    def resource_path_of(self, library_name):
        library = self.get_a_plugin(library_name)
        return library.resources_path


class EngineFactory(PluginManager):
    def __init__(self):
        super(EngineFactory, self).__init__(
            constants.TEMPLATE_ENGINE_EXTENSION
        )

    def get_engine(self, template_type):
        return self.load_me_now(template_type)

    def all_types(self):
        return list(self.registry.keys())

    def raise_exception(self, key):
        raise exceptions.NoThirdPartyEngine(key)


LIBRARIES = LibraryManager()
ENGINES = EngineFactory()


def expand_template_directories(dirs):
    if not isinstance(dirs, list):
        dirs = [dirs]

    for directory in dirs:
        yield expand_template_directory(directory)


def expand_template_directory(directory):
    translated_directory = None
    if ":" in directory:
        library_or_repo_name, relative_path = directory.split(":")
        potential_repo_path = os.path.join(
            utils.get_moban_home(), library_or_repo_name
        )
        if os.path.exists(potential_repo_path):
            # expand repo template path
            if relative_path:
                translated_directory = os.path.join(
                    potential_repo_path, relative_path
                )
            else:
                translated_directory = potential_repo_path
        else:
            # expand pypi template path
            library_path = LIBRARIES.resource_path_of(library_or_repo_name)
            if relative_path:
                translated_directory = os.path.join(
                    library_path, relative_path
                )
            else:
                translated_directory = library_path
    else:
        # local template path
        translated_directory = os.path.abspath(directory)
    return translated_directory
