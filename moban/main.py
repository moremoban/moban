"""
    moban
    ~~~~~~~~~~~~~~~~~~~

    Bring jinja2 to command line

    :copyright: (c) 2016-2019 by Onni Software Ltd.
    :license: MIT License, see LICENSE for more details

"""
import sys
import argparse

from moban import plugins, reporter, constants, mobanfile, exceptions
from moban.utils import merge
from moban._version import __version__
from moban.hashstore import HASH_STORE
from moban.data_loaders.manager import load_data


def main():
    """
    program entry point
    """
    parser = create_parser()
    options = vars(parser.parse_args())
    HASH_STORE.IGNORE_CACHE_FILE = options[constants.LABEL_FORCE]
    moban_file = options[constants.LABEL_MOBANFILE]
    load_engine_factory_and_engines()  # Error: jinja2 if removed
    if moban_file is None:
        moban_file = mobanfile.find_default_moban_file()
    if moban_file:
        try:
            count = handle_moban_file(moban_file, options)
            moban_exit(options[constants.LABEL_EXIT_CODE], count)
        except (
            exceptions.DirectoryNotFound,
            exceptions.NoThirdPartyEngine,
            exceptions.MobanfileGrammarException,
        ) as e:
            reporter.report_error_message(str(e))
            moban_exit(options[constants.LABEL_EXIT_CODE], constants.ERROR)
    else:
        try:
            count = handle_command_line(options)
            moban_exit(options[constants.LABEL_EXIT_CODE], count)
        except exceptions.NoTemplate as e:
            reporter.report_error_message(str(e))
            moban_exit(options[constants.LABEL_EXIT_CODE], constants.ERROR)


def moban_exit(exit_code_toggle_flag, exit_code):
    if exit_code_toggle_flag:
        if exit_code:
            sys.exit(exit_code)
    else:
        if exit_code == constants.ERROR:
            sys.exit(1)


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
        "--%s" % constants.LABEL_EXIT_CODE,
        action="store_true",
        dest=constants.LABEL_EXIT_CODE,
        default=False,
        help="tell moban to change exit code",
    )
    parser.add_argument(
        "-m", "--%s" % constants.LABEL_MOBANFILE, help="custom moban file"
    )
    parser.add_argument(
        "-g", "--%s" % constants.LABEL_GROUP, help="a subset of targets"
    )
    parser.add_argument(
        constants.POSITIONAL_LABEL_TEMPLATE,
        metavar="template",
        type=str,
        nargs="?",
        help="string templates",
    )
    parser.add_argument(
        "-v",
        "--%s" % constants.LABEL_VERSION,
        action="version",
        version="%(prog)s {v}".format(v=__version__),
    )
    return parser


def handle_moban_file(moban_file, options):
    """
    act upon default moban file
    """
    moban_file_configurations = load_data(None, moban_file)
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
    check_none(moban_file_configurations, moban_file)
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


def check_none(data, moban_file):
    """
    check whether the yaml data has empty value such as:
    """
    if isinstance(data, dict):
        for k, v in data.items():
            if check_none(v, moban_file) is None:
                loc = data.lc.key(k)
                raise exceptions.MobanfileGrammarException(
                    constants.ERROR_MALFORMED_YAML
                    % (moban_file, loc[0] + 1)  # line number starts from 0
                )
    elif isinstance(data, list):
        for i, x in enumerate(data):
            if check_none(x, moban_file) is None:
                loc = data.lc.item(i)
                raise exceptions.MobanfileGrammarException(
                    constants.ERROR_MALFORMED_YAML % (moban_file, loc[0] + 1)
                )
    return data


def handle_command_line(options):
    """
    act upon command options
    """
    options = merge(options, constants.DEFAULT_OPTIONS)
    engine = plugins.ENGINES.get_engine(
        options[constants.LABEL_TEMPLATE_TYPE],
        options[constants.LABEL_TMPL_DIRS],
        options[constants.LABEL_CONFIG_DIR],
    )
    if options[constants.LABEL_TEMPLATE] is None:
        if options[constants.POSITIONAL_LABEL_TEMPLATE] is None:
            raise exceptions.NoTemplate(constants.ERROR_NO_TEMPLATE)
        else:
            engine.render_string_to_file(
                options[constants.POSITIONAL_LABEL_TEMPLATE],
                options[constants.LABEL_CONFIG],
                options[constants.LABEL_OUTPUT],
            )
    else:
        engine.render_to_file(
            options[constants.LABEL_TEMPLATE],
            options[constants.LABEL_CONFIG],
            options[constants.LABEL_OUTPUT],
        )
    engine.report()
    HASH_STORE.save_hashes()
    exit_code = reporter.convert_to_shell_exit_code(
        engine.number_of_templated_files()
    )
    return exit_code


def load_engine_factory_and_engines():
    plugins.make_sure_all_pkg_are_loaded()
