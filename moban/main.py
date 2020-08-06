"""
    moban
    ~~~~~~~~~~~~~~~~~~~

    Bring jinja2 to command line

    :copyright: (c) 2016-2020 by Onni Software Ltd.
    :license: MIT License, see LICENSE for more details

"""
import sys
import logging
import argparse
import logging.config
from io import StringIO
from collections import defaultdict

from ruamel.yaml import YAML

from moban import constants, exceptions
from moban.core import ENGINES, plugins, hashstore, mobanfile, data_loader
from moban._version import __version__
from moban.externals import reporter, file_system
from moban.core.utils import handle_plugin_dirs
from moban.program_options import OPTIONS

LOG = logging.getLogger()
LOG_LEVEL = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]


def main():
    parser = create_parser()
    options = vars(parser.parse_args())
    handle_verbose(options[constants.LABEL_VERBOSE])
    load_engine_factory_and_engines()  # Error: jinja2 if removed
    hashstore.HASH_STORE.IGNORE_CACHE_FILE = options[constants.LABEL_FORCE]
    options[constants.CLI_DICT] = handle_custom_variables(
        options.pop(constants.LABEL_DEFINE)
    )
    handle_custom_extensions(options.pop(constants.LABEL_EXTENSION))
    handle_plugin_dirs(options.pop(constants.LABEL_PLUGIN_DIRS))

    OPTIONS.update(options)
    moban_file = options[constants.LABEL_MOBANFILE]
    if moban_file is None:
        moban_file = find_default_moban_file()
    if moban_file:
        try:
            count = handle_moban_file(moban_file, options)
            moban_exit(options[constants.LABEL_EXIT_CODE], count)
        except (
            exceptions.DirectoryNotFound,
            exceptions.NoThirdPartyEngine,
            exceptions.MobanfileGrammarException,
            exceptions.UnsupportedPyFS2Protocol,
        ) as e:
            LOG.exception(e)
            reporter.report_error_message(str(e))
            moban_exit(options[constants.LABEL_EXIT_CODE], constants.ERROR)
    else:
        try:
            count = handle_command_line(options)
            moban_exit(options[constants.LABEL_EXIT_CODE], count)
        except (
            exceptions.NoTemplate,
            exceptions.UnsupportedPyFS2Protocol,
        ) as e:
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
    parser = argparse.ArgumentParser(
        prog=constants.PROGRAM_NAME, description=constants.PROGRAM_DESCRIPTION
    )
    parser.add_argument(
        "-c", "--%s" % constants.LABEL_CONFIG, help="the data file"
    )
    parser.add_argument(
        "-t", "--%s" % constants.LABEL_TEMPLATE, help="the template file"
    )
    parser.add_argument(
        "-o", "--%s" % constants.LABEL_OUTPUT, help="the output file"
    )
    parser.add_argument(
        constants.POSITIONAL_LABEL_TEMPLATE,
        metavar="template",
        type=str,
        nargs="?",
        help="string templates",
    )
    advanced = parser.add_argument_group(
        "Advanced options", "For better control"
    )
    advanced.add_argument(
        "-td",
        f"--{constants.LABEL_TMPL_DIRS}",
        nargs="*",
        help="add more directories for template file lookup",
    )
    advanced.add_argument(
        "-cd",
        f"--{constants.LABEL_CONFIG_DIR}",
        help="the directory for configuration file lookup",
    )
    advanced.add_argument(
        "-pd",
        f"--{constants.LABEL_PLUGIN_DIRS}",
        nargs="*",
        help="add more directories for plugin lookup",
    )
    advanced.add_argument(
        "-m", "--%s" % constants.LABEL_MOBANFILE, help="custom moban file"
    )
    advanced.add_argument(
        "-g", "--%s" % constants.LABEL_GROUP, help="a subset of targets"
    )
    advanced.add_argument(
        f"--{constants.LABEL_TEMPLATE_TYPE.replace('_', '-')}",
        help="the template type, default is jinja2",
    )
    advanced.add_argument(
        "-d",
        f"--{constants.LABEL_DEFINE}",
        nargs="+",
        help=(
            "to supply additional or override predefined variables,"
            + " format: VAR=VALUEs"
        ),
    )
    advanced.add_argument(
        "-e",
        f"--{constants.LABEL_EXTENSION}",
        nargs="+",
        help="to to TEMPLATE_TYPE=EXTENSION_NAME",
    )
    advanced.add_argument(
        "-f",
        action="store_true",
        dest=constants.LABEL_FORCE,
        default=False,
        help="force moban to template all files despite of .moban.hashes",
    )
    developer = parser.add_argument_group(
        "Developer options", "For debugging and development"
    )
    developer.add_argument(
        f"--{constants.LABEL_EXIT_CODE}",
        action="store_true",
        dest=constants.LABEL_EXIT_CODE,
        default=False,
        help=(
            "by default, exist code 0 means no error, 1 means error occured. "
            + "It tells moban to change 1 for changes, 2 for error occured"
        ),
    )
    developer.add_argument(
        "-V",
        f"--{constants.LABEL_VERSION}",
        action="version",
        version="%(prog)s {v}".format(v=__version__),
    )
    developer.add_argument(
        "-v",
        action="count",
        dest=constants.LABEL_VERBOSE,
        default=0,
        help="show verbose, try -v, -vv, -vvv",
    )
    return parser


def handle_moban_file(moban_file, options):
    """
    act upon default moban file
    """
    moban_file_configurations = data_loader.load_data(None, moban_file)
    yaml = YAML(typ="rt")
    dumped_yaml = StringIO()
    yaml.dump(moban_file_configurations, dumped_yaml)
    LOG.info(dumped_yaml.getvalue())
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
    hashstore.HASH_STORE.save_hashes()


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
    reporter.GLOBAL["PRINT"] = False
    options = data_loader.merge(options, constants.DEFAULT_OPTIONS)
    engine = ENGINES.get_engine(
        options[constants.LABEL_TEMPLATE_TYPE],
        options[constants.LABEL_TMPL_DIRS],
        options[constants.LABEL_CONFIG_DIR],
    )
    if options[constants.LABEL_TEMPLATE] is None:
        content = options[constants.POSITIONAL_LABEL_TEMPLATE]
        if content is None:
            if not sys.stdin.isatty() and sys.platform != "win32":
                content = sys.stdin.read().strip()
        if content is None:
            raise exceptions.NoTemplate(constants.ERROR_NO_TEMPLATE)

        engine.render_string_to_file(
            content,
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
    hashstore.HASH_STORE.save_hashes()
    exit_code = reporter.convert_to_shell_exit_code(
        engine.number_of_templated_files()
    )
    return exit_code


def find_default_moban_file():
    for moban_file in constants.DEFAULT_MOBAN_FILES:
        if file_system.exists(moban_file):
            break
    else:
        moban_file = None
    return moban_file


def load_engine_factory_and_engines():
    plugins.make_sure_all_pkg_are_loaded()


def handle_custom_variables(list_of_definitions):
    custom_data = {}
    if list_of_definitions:
        for definition in list_of_definitions:
            key, value = definition.split("=")
            custom_data[key] = value

    return custom_data


def handle_custom_extensions(list_of_definitions):
    user_extensions = defaultdict(set)
    if list_of_definitions:
        for definition in list_of_definitions:
            key, value = definition.split("=")
            user_extensions[key].add(value)
    ENGINES.register_extensions(user_extensions)


def handle_verbose(verbose_level):
    if verbose_level > len(LOG_LEVEL):
        verbose_level = len(LOG_LEVEL) - 1
    level = LOG_LEVEL[verbose_level]
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=level,
    )
