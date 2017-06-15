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

from moban.utils import merge, open_yaml, HashStore
from moban.engine import EngineFactory
import moban.constants as constants
from moban.mobanfile import handle_moban_file_v1


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
    options = vars(parser.parse_args())
    HashStore.IGNORE_CACHE_FILE = options['force']
    if os.path.exists(constants.DEFAULT_MOBAN_FILE):
        handle_moban_file(options)
    else:
        handle_command_line(options)


def create_parser():
    """
    construct the program options
    """
    parser = argparse.ArgumentParser(
        prog=constants.PROGRAM_NAME,
        description=constants.PROGRAM_DESCRIPTION)
    parser.add_argument(
        '-cd', '--%s' % constants.LABEL_CONFIG_DIR,
        help="the directory for configuration file lookup"
    )
    parser.add_argument(
        '-c', '--%s' % constants.LABEL_CONFIG,
        help="the dictionary file"
    )
    parser.add_argument(
        '-td', '--%s' % constants.LABEL_TMPL_DIRS, nargs="*",
        help="the directories for template file lookup"
    )
    parser.add_argument(
        '-t', '--%s' % constants.LABEL_TEMPLATE,
        help="the template file"
    )
    parser.add_argument(
        '-o', '--%s' % constants.LABEL_OUTPUT,
        help="the output file"
    )
    parser.add_argument(
        '--%s' % constants.LABEL_TEMPLATE_TYPE,
        help="the template type, default is jinja2"
    )
    parser.add_argument(
        '-f', action='store_true', dest='force', default=False,
        help="force moban to template all files despite of .moban.hashes"
    )
    return parser


def handle_moban_file(options):
    """
    act upon default moban file
    """
    moban_file_configurations = open_yaml(
        None,
        constants.DEFAULT_MOBAN_FILE)
    if moban_file_configurations is None:
        print(ERROR_INVALID_MOBAN_FILE % constants.DEFAULT_MOBAN_FILE)
        sys.exit(-1)
    if constants.LABEL_TARGETS not in moban_file_configurations:
        print(ERROR_NO_TARGETS % constants.DEFAULT_MOBAN_FILE)
        sys.exit(0)
    version = moban_file_configurations.get(
        constants.MOBAN_VERSION,
        constants.DEFAULT_MOBAN_VERSION
    )
    if version == constants.DEFAULT_MOBAN_VERSION:
        handle_moban_file_v1(moban_file_configurations, options)
    else:
        raise NotImplementedError(
            "moban file version %d is not supported" % version)


def handle_command_line(options):
    """
    act upon command options
    """
    options = merge(options, constants.DEFAULT_OPTIONS)
    if options[constants.LABEL_TEMPLATE] is None:
        print(ERROR_NO_TEMPLATE)
        sys.exit(-1)
    engine_class = EngineFactory.get_engine(
        options[constants.LABEL_TEMPLATE_TYPE])
    engine = engine_class(options[constants.LABEL_TMPL_DIRS],
                          options[constants.LABEL_CONFIG_DIR])
    engine.render_to_file(
        options[constants.LABEL_TEMPLATE],
        options[constants.LABEL_CONFIG],
        options[constants.LABEL_OUTPUT]
    )
