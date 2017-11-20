import os


# Configurations
PROGRAM_NAME = 'moban'
PROGRAM_DESCRIPTION = ('Yet another jinja2 cli command for static ' +
                       'text generation')
DEFAULT_YAML_SUFFIX = '.yml'
# .moban.yml, default moban configuration file
DEFAULT_MOBAN_FILES = [
    '.%s%s' % (PROGRAM_NAME, DEFAULT_YAML_SUFFIX),
    '.%s%s' % (PROGRAM_NAME, '.yaml')
]
DEFAULT_TEMPLATE_TYPE = 'jinja2'

# .moban.hashes
DEFAULT_MOBAN_CACHE_FILE = '.moban.hashes'

# Command line options
LABEL_CONFIG = 'configuration'
LABEL_CONFIG_DIR = 'configuration_dir'
LABEL_TEMPLATE = 'template'
LABEL_TMPL_DIRS = 'template_dir'
LABEL_OUTPUT = 'output'
LABEL_TEMPLATE_TYPE = 'template_type'
LABEL_TARGETS = 'targets'
LABEL_OVERRIDES = 'overrides'

DEFAULT_CONFIGURATION_DIRNAME = '.moban.cd'
DEFAULT_TEMPLATE_DIRNAME = '.moban.td'
DEFAULT_OPTIONS = {
    # .moban.cd, default configuration dir
    LABEL_CONFIG_DIR: os.path.join('.', DEFAULT_CONFIGURATION_DIRNAME),
    # .moban.td, default template dirs
    LABEL_TMPL_DIRS: ['.', os.path.join('.', DEFAULT_TEMPLATE_DIRNAME)],
    # moban.output, default output file name
    LABEL_OUTPUT: '%s.output' % PROGRAM_NAME,
    # data.yml, default data input file
    LABEL_CONFIG: 'data%s' % DEFAULT_YAML_SUFFIX,
    LABEL_TEMPLATE_TYPE: DEFAULT_TEMPLATE_TYPE
}

# moban file version
MOBAN_VERSION = "moban_file_spec_version"
DEFAULT_MOBAN_VERSION = '1.0'

# error messages
ERROR_DATA_FILE_NOT_FOUND = "Both %s and %s does not exist"
ERROR_DATA_FILE_ABSENT = "File %s does not exist"

MESSAGE_SYNTAX_ERROR = "%s already exists in the target %s"
MESSAGE_DIR_NOT_EXIST = "%s does not exist"
MESSAGE_NO_THIRD_PARTY_ENGINE = "No such template support"
MESSAGE_FILE_VERSION_NOT_SUPPORTED = "moban file version '%s' is not supported"

# I/O messages
# Error handling
ERROR_INVALID_MOBAN_FILE = "%s is an invalid yaml file."
ERROR_NO_TARGETS = "No targets in %s"
ERROR_NO_TEMPLATE = "No template found"
