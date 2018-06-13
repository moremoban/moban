"""
    moban
    ~~~~~~~~~~~~~~~~~~~

    Bring jinja2 to command line

    :copyright: (c) 2016-2017 by Onni Software Ltd.
    :license: MIT License, see LICENSE for more details

"""

import sys
import argparse

from moban.utils import merge, open_yaml
from moban.hashstore import HASH_STORE
from moban.engine import ENGINES
import moban.constants as constants
import moban.mobanfile as mobanfile
import moban.exceptions as exceptions
import moban.reporter as reporter


def main():
    """
    program entry point
    """
    parser = create_parser()
    options = vars(parser.parse_args())
    HASH_STORE.IGNORE_CACHE_FILE = options[constants.LABEL_FORCE]
    moban_file = options[constants.LABEL_MOBANFILE]
    if moban_file is None:
        moban_file = mobanfile.find_default_moban_file()
    if moban_file:
        try:
            count = handle_moban_file(moban_file, options)
            if count:
                sys.exit(count)
        except (
            exceptions.DirectoryNotFound,
            exceptions.NoThirdPartyEngine,
            exceptions.MobanfileGrammarException,
        ) as e:
            reporter.report_error_message(str(e))
            sys.exit(constants.ERROR)
    else:
        try:
            count = handle_command_line(options)
            if count:
                sys.exit(count)
        except exceptions.NoTemplate as e:
            reporter.report_error_message(str(e))
            sys.exit(constants.ERROR)


def create_parser():
    """
    construct the program options
    """
    parser = argparse.ArgumentParser(
        prog=constants.PROGRAM_NAME, description=constants.PROGRAM_DESCRIPTION
    )
    parser.add_argument(
        "-cd",
        "--%s" % constants.LABEL_CONFIG_DIR,
        help="the directory for configuration file lookup",
    )
    parser.add_argument(
        "-c", "--%s" % constants.LABEL_CONFIG, help="the dictionary file"
    )
    parser.add_argument(
        "-td",
        "--%s" % constants.LABEL_TMPL_DIRS,
        nargs="*",
        help="the directories for template file lookup",
    )
    parser.add_argument(
        "-t", "--%s" % constants.LABEL_TEMPLATE, help="the template file"
    )
    parser.add_argument(
        "-o", "--%s" % constants.LABEL_OUTPUT, help="the output file"
    )
    parser.add_argument(
        "--%s" % constants.LABEL_TEMPLATE_TYPE,
        help="the template type, default is jinja2",
    )
    parser.add_argument(
        "-f",
        action="store_true",
        dest=constants.LABEL_FORCE,
        default=False,
        help="force moban to template all files despite of .moban.hashes",
    )
    parser.add_argument(
        "-m", "--%s" % constants.LABEL_MOBANFILE, help="custom moban file"
    )
    return parser


def handle_moban_file(moban_file, options):
    """
    act upon default moban file
    """
    moban_file_configurations = open_yaml(None, moban_file)
    if moban_file_configurations is None:
        raise exceptions.MobanfileGrammarException(
            constants.ERROR_INVALID_MOBAN_FILE % moban_file
        )
    if (
        constants.LABEL_TARGETS not in moban_file_configurations
        and constants.LABEL_COPY not in moban_file_configurations
    ):
        raise exceptions.MobanfileGrammarException(
            constants.ERROR_NO_TARGETS % moban_file
        )
    version = moban_file_configurations.get(
        constants.MOBAN_VERSION, constants.DEFAULT_MOBAN_VERSION
    )
    if version == constants.DEFAULT_MOBAN_VERSION:
        mobanfile.handle_moban_file_v1(moban_file_configurations, options)
    else:
        raise exceptions.MobanfileGrammarException(
            constants.MESSAGE_FILE_VERSION_NOT_SUPPORTED % version
        )
    HASH_STORE.save_hashes()


def handle_command_line(options):
    """
    act upon command options
    """
    options = merge(options, constants.DEFAULT_OPTIONS)
    if options[constants.LABEL_TEMPLATE] is None:
        raise exceptions.NoTemplate(constants.ERROR_NO_TEMPLATE)
    engine_class = ENGINES.get_engine(
        options[constants.LABEL_TEMPLATE_TYPE]
    )
    engine = engine_class(
        options[constants.LABEL_TMPL_DIRS], options[constants.LABEL_CONFIG_DIR]
    )
    engine.render_to_file(
        options[constants.LABEL_TEMPLATE],
        options[constants.LABEL_CONFIG],
        options[constants.LABEL_OUTPUT],
    )
    HASH_STORE.save_hashes()
    exit_code = reporter.convert_to_shell_exit_code(
        engine.number_of_templated_files()
    )
    return exit_code
