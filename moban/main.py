"""
    moban
    ~~~~~~~~~~~~~~~~~~~

    Bring jinja2 to command line

    :copyright: (c) 2016 by Onni Software Ltd.
    :license: MIT License, see LICENSE for more details

"""

import os
import sys
import argparse

from moban.context import merge, open_yaml
from moban.engine import Engine

# Configurations
PROGRAM_NAME = 'moban'
PROGRAM_DESCRIPTION = 'Yet another jinja2 cli command for static text generation'
DEFAULT_YAML_SUFFIX = '.yml'
# .moban.yml, default moban configuration file
DEFAULT_MOBAN_FILE = '.%s%s' % (PROGRAM_NAME, DEFAULT_YAML_SUFFIX)

# Command line options
LABEL_CONFIG = 'configuration'
LABEL_CONFIG_DIR = '%s_dir' % LABEL_CONFIG
LABEL_TEMPLATE = 'template'
LABEL_TMPL_DIRS = '%s_dir' % LABEL_TEMPLATE
LABEL_OUTPUT = 'output'
LABEL_TARGETS = 'targets'
DEFAULT_OPTIONS = {
    # .moban.cd, default configuration dir
    LABEL_CONFIG_DIR: os.path.join('.', '.%s.cd' % PROGRAM_NAME),
    # .moban.td, default template dirs
    LABEL_TMPL_DIRS: ['.', os.path.join('.', '.%s.td' % PROGRAM_NAME)],
    # moban.output, default output file name
    LABEL_OUTPUT: '%s.output' % PROGRAM_NAME,
    # data.yml, default data input file
    LABEL_CONFIG: 'data%s' % DEFAULT_YAML_SUFFIX
}

# I/O messages
# Error handling
ERROR_INVALID_MOBAN_FILE = "%s is an invalid yaml file."
ERROR_NO_TARGETS = "No targets in %s"
ERROR_NO_TEMPLATE = "No template found"


def main():
    """
    program entry point
    """
    parser = create_parser()
    if os.path.exists(DEFAULT_MOBAN_FILE):
        handle_moban_file(parser)
    else:
        handle_command_line(parser)


def create_parser():
    """
    construct the program options
    """
    parser = argparse.ArgumentParser(
        prog=PROGRAM_NAME,
        description=PROGRAM_DESCRIPTION)
    parser.add_argument(
        '-cd', '--%s' % LABEL_CONFIG_DIR,
        help="the directory for configuration file lookup"
    )
    parser.add_argument(
        '-c', '--%s' % LABEL_CONFIG,
        help="the dictionary file"
    )
    parser.add_argument(
        '-td', '--%s' % LABEL_TMPL_DIRS, nargs="*",
        help="the directories for template file lookup"
    )
    parser.add_argument(
        '-t', '--%s' % LABEL_TEMPLATE,
        help="the template file"
    )
    parser.add_argument(
        '-o', '--%s' % LABEL_OUTPUT,
        help="the output file"
    )
    return parser


def handle_moban_file(parser):
    """
    act upon default moban file
    """
    options = {}
    if len(sys.argv) > 1:
        options = vars(parser.parse_args())
    more_options = open_yaml(None, DEFAULT_MOBAN_FILE)
    if more_options is None:
        print(ERROR_INVALID_MOBAN_FILE % DEFAULT_MOBAN_FILE)
        sys.exit(-1)
    if LABEL_TARGETS not in more_options:
        print(ERROR_NO_TARGETS % DEFAULT_MOBAN_FILE)
        sys.exit(0)
    if LABEL_CONFIG in more_options:
        options = merge(options, more_options[LABEL_CONFIG])
    options = merge(options, DEFAULT_OPTIONS)
    list_of_templating_parameters = translate_targets(
        options,
        more_options[LABEL_TARGETS])    
    engine = Engine(options[LABEL_TMPL_DIRS], options[LABEL_CONFIG_DIR])
    engine.render_to_files(list_of_templating_parameters)


def handle_command_line(parser):
    """
    act upon command options
    """
    options = vars(parser.parse_args())
    options = merge(options, DEFAULT_OPTIONS)
    if options[LABEL_TEMPLATE] is None:
        print(ERROR_NO_TEMPLATE)
        parser.print_help()
        sys.exit(-1)
    engine = Engine(options[LABEL_TMPL_DIRS], options[LABEL_CONFIG_DIR])
    engine.render_to_file(
        options[LABEL_TEMPLATE],
        options[LABEL_CONFIG],
        options[LABEL_OUTPUT]
    )


def translate_targets(options, targets):
    common_data_file = options[LABEL_CONFIG]
    for target in targets:
        if LABEL_OUTPUT in target:
            template_file = target.get(LABEL_TEMPLATE,
                                       options.get(LABEL_TEMPLATE, None))
            data_file = target.get(LABEL_CONFIG, common_data_file)
            output = target[LABEL_OUTPUT]
            yield((template_file, data_file, output))
        else:
            for output, template_file in target.items():
                yield((template_file, common_data_file, output))
