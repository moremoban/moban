import os

# Configurations
PROGRAM_NAME = "moban"
PROGRAM_DESCRIPTION = (
    "Yet another jinja2 cli command for static " + "text generation"
)
DEFAULT_YAML_SUFFIX = ".yml"
# .moban.yml, default moban configuration file
DEFAULT_MOBAN_FILES = [
    ".%s%s" % (PROGRAM_NAME, DEFAULT_YAML_SUFFIX),
    ".%s%s" % (PROGRAM_NAME, ".yaml"),
]
DEFAULT_TEMPLATE_TYPE = "jinja2"
DEFAULT_DATA_TYPE = "yaml"
ACTION_COPY = "copy"
DEFAULT_ACTION = ACTION_TEMPLATE = "template"

# .moban.hashes
DEFAULT_MOBAN_CACHE_FILE = ".moban.hashes"

# Command line options
LABEL_CONFIG = "configuration"
LABEL_CONFIG_DIR = "configuration_dir"
LABEL_PLUGIN_DIRS = "plugin_dir"
LABEL_TEMPLATE = "template"
POSITIONAL_LABEL_TEMPLATE = "template_in_string"
LABEL_TMPL_DIRS = "template_dir"
LABEL_EXIT_CODE = "exit-code"
LABEL_OUTPUT = "output"
LABEL_TEMPLATE_TYPE = "template_type"
LABEL_OVERRIDES = "overrides"
LABEL_MOBANFILE = "mobanfile"
LABEL_FORCE = "force"
LABEL_VERSION = "version"


DEFAULT_CONFIGURATION_DIRNAME = ".moban.cd"
DEFAULT_TEMPLATE_DIRNAME = ".moban.td"
DEFAULT_OPTIONS = {
    # .moban.cd, default configuration dir
    LABEL_CONFIG_DIR: os.path.join(".", DEFAULT_CONFIGURATION_DIRNAME),
    # .moban.td, default template dirs
    LABEL_TMPL_DIRS: [".", os.path.join(".", DEFAULT_TEMPLATE_DIRNAME)],
    # moban.output, default output file name
    LABEL_OUTPUT: "%s.output" % PROGRAM_NAME,
    # data.yml, default data input file
    LABEL_CONFIG: "data%s" % DEFAULT_YAML_SUFFIX,
    LABEL_TEMPLATE_TYPE: DEFAULT_TEMPLATE_TYPE,
}

# moban file version
MOBAN_VERSION = "moban_file_spec_version"
DEFAULT_MOBAN_VERSION = "1.0"
MOBAN_DIR_NAME_UNDER_USER_HOME = ".moban"
MOBAN_REPOS_DIR_NAME = "repos"
# moban file configuration
LABEL_REQUIRES = "requires"
LABEL_TARGETS = "targets"
LABEL_COPY = "copy"
LABEL_EXTENSIONS = "extensions"
LABEL_ACTION = "action"
LABEL_SOURCE = "source"
LABEL_DEST = "dest"

# error messages
ERROR_DATA_FILE_NOT_FOUND = "Both %s and %s does not exist"
ERROR_DATA_FILE_ABSENT = "File %s does not exist"

MESSAGE_SYNTAX_ERROR = "%s already exists in the target %s"
MESSAGE_DIR_NOT_EXIST = "%s does not exist"
MESSAGE_NO_THIRD_PARTY_ENGINE = "No such template support"
MESSAGE_FILE_VERSION_NOT_SUPPORTED = "moban file version '%s' is not supported"
MESSAGE_INVALID_GIT_URL = 'An invalid git url: "%s" in mobanfile'

# deprecation message
MESSAGE_DEPRECATE_COPY_SINCE_0_4_0 = (
    "'copy:' is deprecated since 0.4.0! " +
    "Please use 'targets:' instead")

# I/O messages
# Error handling
ERROR_INVALID_MOBAN_FILE = "%s is an invalid yaml file."
ERROR_NO_TARGETS = "No targets in %s"
ERROR_NO_TEMPLATE = "No template found"
ERROR_MALFORMED_YAML = "Empty value in %s at line %s"


# Shell messages
HAS_CHANGES = 1
ERROR = 2
NO_CHANGES = 0

# Require
GIT_REQUIRE = "GIT"
GIT_HAS_SUBMODULE = "submodule"
GIT_URL = "url"
GIT_BRANCH = "branch"
PYPI_REQUIRE = "PYPI"
PYPI_PACKAGE_NAME = "name"
REQUIRE_TYPE = "type"


# Extension
JINJA_FILTER_EXTENSION = "jinja_filter"
JINJA_TEST_EXTENSION = "jinja_test"
JINJA_GLOBALS_EXTENSION = "jinja_globals"

TEMPLATE_ENGINE_EXTENSION = "template_engine"
DATA_LOADER_EXTENSION = "data_loader"
LIBRARY_EXTENSION = "library"

MOBAN_EXTENSIONS = "^moban_.+$"
MOBAN_TEMPLATES = "^.+_mobans_pkg$"
MOBAN_ALL = "%s|%s" % (MOBAN_EXTENSIONS, MOBAN_TEMPLATES)
