import logging
from collections import OrderedDict

from moban import core, constants
from moban.externals import reporter
from moban.core.utils import (
    handle_plugin_dirs,
    verify_the_existence_of_directories,
)
from moban.deprecated import handle_copy, handle_requires
from moban.core.data_loader import merge
from moban.core.moban_factory import expand_template_directories
from moban.core.mobanfile.targets import (
    parse_targets,
    extract_target,
    extract_group_targets,
)
from .store import STORE

LOG = logging.getLogger(__name__)


def handle_moban_file_v1(moban_file_configurations, command_line_options):
    LOG.info("handling moban file")
    merged_options = None

    targets = moban_file_configurations.get(constants.LABEL_TARGETS, [])
    if constants.LABEL_COPY in moban_file_configurations:
        legacy_copy_targets = handle_copy(
            merged_options, moban_file_configurations[constants.LABEL_COPY]
        )
        targets += legacy_copy_targets

    cli_target = extract_target(command_line_options)
    group_target = command_line_options.get(constants.LABEL_GROUP)
    if group_target:
        # will raise exception when group target not found
        targets = extract_group_targets(group_target, targets)

    if constants.LABEL_CONFIG in moban_file_configurations:
        merged_options = merge(
            command_line_options,
            moban_file_configurations[constants.LABEL_CONFIG],
        )
    merged_options = merge(command_line_options, constants.DEFAULT_OPTIONS)

    plugins_dirs = merged_options.get(constants.LABEL_PLUGIN_DIRS)

    if plugins_dirs:
        handle_plugin_dirs(plugins_dirs)

    # deprecated
    requires = moban_file_configurations.get(constants.LABEL_REQUIRES)
    if requires:
        handle_requires(requires)

    # call expand template directory always after handle require please
    # the penalty is: newly clone repos are not visible
    # one more note: verify_the_existence_of_directories will remove non-exist dirs
    merged_options[
        constants.LABEL_TMPL_DIRS
    ] = verify_the_existence_of_directories(
        list(
            expand_template_directories(
                merged_options[constants.LABEL_TMPL_DIRS]
            )
        )
    )

    extensions = moban_file_configurations.get(constants.LABEL_EXTENSIONS)
    if extensions:
        core.ENGINES.register_extensions(extensions)

    template_types = merged_options.get(constants.LABEL_TEMPLATE_TYPES)
    if template_types:
        core.ENGINES.register_options(template_types)

    if cli_target:
        number_of_templated_files = handle_targets(
            merged_options, [cli_target]
        )
    elif targets:
        number_of_templated_files = handle_targets(merged_options, targets)
    else:
        number_of_templated_files = 0

    exit_code = reporter.convert_to_shell_exit_code(number_of_templated_files)
    reporter.report_up_to_date()
    return exit_code


def handle_targets(merged_options, targets):
    LOG.info("handling targets")
    parse_targets(merged_options, targets)
    list_of_templating_parameters = STORE.targets
    jobs_for_each_engine = OrderedDict()

    for target in list_of_templating_parameters:
        forced_template_type = merged_options.get(
            constants.LABEL_FORCE_TEMPLATE_TYPE
        )
        if forced_template_type:
            target.set_template_type(forced_template_type)

        template_type = target.template_type
        primary_template_type = core.ENGINES.get_primary_key(template_type)
        if primary_template_type is None:
            primary_template_type = merged_options[
                constants.LABEL_TEMPLATE_TYPE
            ]
            target.set_template_type(primary_template_type)

        if primary_template_type not in jobs_for_each_engine:
            jobs_for_each_engine[primary_template_type] = []

        jobs_for_each_engine[primary_template_type].append(target)

    count = 0
    fall_out_targets = []
    for template_type in jobs_for_each_engine.keys():
        engine = core.ENGINES.get_engine(
            template_type,
            merged_options[constants.LABEL_TMPL_DIRS],
            merged_options[constants.LABEL_CONFIG_DIR],
        )
        engine.render_to_files(jobs_for_each_engine[template_type])
        engine.report()
        count = count + engine.number_of_templated_files()
        fall_out_targets += engine.fall_out_targets

    if fall_out_targets:
        copy_engine = core.ENGINES.get_engine(
            constants.TEMPLATE_COPY,
            merged_options[constants.LABEL_TMPL_DIRS],
            merged_options[constants.LABEL_CONFIG_DIR],
        )
        copy_engine.render_to_files(fall_out_targets)
        copy_engine.report()
        count = count + copy_engine.number_of_templated_files()
    return count
