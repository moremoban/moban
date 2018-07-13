import os
import re
import sys
from collections import defaultdict

from lml.utils import do_import

import moban.constants as constants
import moban.reporter as reporter
from moban.engine import ENGINES
from moban.utils import merge, parse_targets, expand_directories
from moban.copier import Copier


def find_default_moban_file():
    for moban_file in constants.DEFAULT_MOBAN_FILES:
        if os.path.exists(moban_file):
            break
    else:
        moban_file = None
    return moban_file


def handle_moban_file_v1(moban_file_configurations, command_line_options):
    merged_options = None
    target = extract_target(command_line_options)
    if constants.LABEL_CONFIG in moban_file_configurations:
        merged_options = merge(
            command_line_options,
            moban_file_configurations[constants.LABEL_CONFIG],
        )
    merged_options = merge(command_line_options, constants.DEFAULT_OPTIONS)
    plugins_dirs = merged_options.get(constants.LABEL_PLUGIN_DIRS)
    if plugins_dirs:
        handle_plugin_dirs(plugins_dirs)

    targets = moban_file_configurations.get(constants.LABEL_TARGETS)
    if targets:
        if target:
            # if command line option exists, append its template to targets
            # issue 30
            targets += target
        number_of_templated_files = handle_targets(merged_options, targets)
    else:
        number_of_templated_files = 0

    if constants.LABEL_COPY in moban_file_configurations:
        number_of_copied_files = handle_copy(
            merged_options[constants.LABEL_TMPL_DIRS],
            moban_file_configurations[constants.LABEL_COPY],
        )
    else:
        number_of_copied_files = 0
    exit_code = reporter.convert_to_shell_exit_code(
        number_of_templated_files + number_of_copied_files
    )
    reporter.report_up_to_date()
    return exit_code


def handle_copy(template_dirs, copy_config):
    copier = Copier(template_dirs)
    copier.copy_files(copy_config)
    copier.report()
    return copier.number_of_copied_files()


def handle_targets(merged_options, targets):
    list_of_templating_parameters = parse_targets(merged_options, targets)
    list_of_templating_parameters = expand_directories(
        list_of_templating_parameters,
        merged_options[constants.LABEL_TMPL_DIRS],
    )
    jobs_for_each_engine = defaultdict(list)
    for file_list in list_of_templating_parameters:
        _, extension = os.path.splitext(file_list[0])
        template_type = extension[1:]
        primary_template_type = ENGINES.get_primary_key(template_type)
        if primary_template_type is None:
            primary_template_type = merged_options[
                constants.LABEL_TEMPLATE_TYPE
            ]
        jobs_for_each_engine[primary_template_type].append(file_list)

    count = 0
    for template_type in jobs_for_each_engine.keys():
        engine_class = ENGINES.get_engine(template_type)
        engine = engine_class(
            merged_options[constants.LABEL_TMPL_DIRS],
            merged_options[constants.LABEL_CONFIG_DIR],
        )
        engine.render_to_files(jobs_for_each_engine[template_type])
        engine.report()
        count = count + engine.number_of_templated_files()
    return count


def handle_plugin_dirs(plugin_dirs):
    for plugin_dir in plugin_dirs:
        plugin_path = os.path.dirname(os.path.abspath(plugin_dir))
        if plugin_path not in sys.path:
            sys.path.append(plugin_path)
        pysearchre = re.compile(".py$", re.IGNORECASE)
        pluginfiles = filter(pysearchre.search, os.listdir(plugin_dir))
        plugins = list(map(lambda fp: os.path.splitext(fp)[0], pluginfiles))
        for plugin in plugins:
            plugin_module = os.path.basename(plugin_dir) + "." + plugin
            do_import(plugin_module)


def extract_target(options):
    template = options.get(constants.LABEL_TEMPLATE)
    config = options.get(constants.LABEL_CONFIG)
    output = options.get(constants.LABEL_OUTPUT)
    result = []
    if template:
        if output is None:
            raise Exception(
                "Please specify a output file name for %s." % template)
        if config:
            result = [
                {
                    constants.LABEL_TEMPLATE: template,
                    constants.LABEL_CONFIG: config,
                    constants.LABEL_OUTPUT: output,
                }
            ]
        else:
            result = [{output: template}]
    return result
