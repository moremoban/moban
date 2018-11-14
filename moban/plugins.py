import os
from moban import utils
from lml.loader import scan_plugins_regex

from moban.extensions import (
    JinjaTestManager,
    JinjaFilterManager,
    JinjaGlobalsManager
)
from moban.extensions import LibraryManager
from moban.engine_factory import EngineFactory
from moban.constants import MOBAN_ALL

LIBRARIES = LibraryManager()
FILTERS = JinjaFilterManager()
TESTS = JinjaTestManager()
GLOBALS = JinjaGlobalsManager()
ENGINES = EngineFactory()

BUILTIN_EXENSIONS = [
    "moban.filters.repr",
    "moban.filters.github",
    "moban.filters.text",
    "moban.tests.files",
]


def refresh_plugins():
    scan_plugins_regex(MOBAN_ALL, "moban", None, BUILTIN_EXENSIONS)


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
