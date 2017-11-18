import os


# Configurations
PROGRAM_NAME = 'moban'
PROGRAM_DESCRIPTION = ('Yet another jinja2 cli command for static ' +
                       'text generation')
DEFAULT_YAML_SUFFIX = '.yml'
# .moban.yml, default moban configuration file
DEFAULT_MOBAN_FILE = '.%s%s' % (PROGRAM_NAME, DEFAULT_YAML_SUFFIX)
DEFAULT_TEMPLATE_TYPE = 'jinja2'

# Command line options
LABEL_CONFIG = 'configuration'
LABEL_CONFIG_DIR = 'configuration_dir'
LABEL_TEMPLATE = 'template'
LABEL_TMPL_DIRS = 'template_dir'
LABEL_OUTPUT = 'output'
LABEL_TEMPLATE_TYPE = 'template_type'
LABEL_TARGETS = 'targets'
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
MOBAN_VERSION = "version"
DEFAULT_MOBAN_VERSION = 1.0
