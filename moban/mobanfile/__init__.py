import os
import re
import sys
from collections import OrderedDict

from moban import plugins, reporter, constants
from lml.utils import do_import
from moban.repo import git_clone
from moban.utils import merge, pip_install
from moban.deprecated import deprecated
from moban.definitions import GitRequire
from moban.plugins.template import expand_template_directories
from moban.mobanfile.targets import parse_targets, extract_group_targets

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


KNOWN_DOMAIN_FOR_GIT = ["github.com", "gitlab.com", "bitbucket.com"]


def find_default_moban_file():
    for moban_file in constants.DEFAULT_MOBAN_FILES:
        if os.path.exists(moban_file):
            break
    else:
        moban_file = None
    return moban_file


def handle_moban_file_v1(moban_file_configurations, command_line_options):
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

    requires = moban_file_configurations.get(constants.LABEL_REQUIRES)
    if requires:
        handle_requires(requires)

    # call expand template directory always after handle require please
    # the penalty is: newly clone repos are not visible
    merged_options[constants.LABEL_TMPL_DIRS] = list(
        expand_template_directories(merged_options[constants.LABEL_TMPL_DIRS])
    )
    extensions = moban_file_configurations.get(constants.LABEL_EXTENSIONS)
    if extensions:
        plugins.ENGINES.register_extensions(extensions)

    template_types = merged_options.get(constants.LABEL_TEMPLATE_TYPES)
    if template_types:
        plugins.ENGINES.register_options(template_types)

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


@deprecated(constants.MESSAGE_DEPRECATE_COPY_SINCE_0_4_0)
def handle_copy(merged_options, copy_config):
    copy_targets = []
    for (dest, src) in _iterate_list_of_dicts(copy_config):
        copy_targets.append(
            {
                constants.LABEL_TEMPLATE: src,
                constants.LABEL_OUTPUT: dest,
                constants.LABEL_TEMPLATE_TYPE: constants.TEMPLATE_COPY,
            }
        )
    return copy_targets


def _iterate_list_of_dicts(list_of_dict):
    for adict in list_of_dict:
        for key, value in adict.items():
            yield (key, value)


def handle_targets(merged_options, targets):
    list_of_templating_parameters = parse_targets(merged_options, targets)
    jobs_for_each_engine = OrderedDict()

    for target in list_of_templating_parameters:
        forced_template_type = merged_options.get(
            constants.LABEL_FORCE_TEMPLATE_TYPE
        )
        if forced_template_type:
            target.set_template_type(forced_template_type)

        template_type = target.template_type
        primary_template_type = plugins.ENGINES.get_primary_key(template_type)
        if primary_template_type is None:
            primary_template_type = merged_options[
                constants.LABEL_TEMPLATE_TYPE
            ]
            target.set_template_type(primary_template_type)

        if primary_template_type not in jobs_for_each_engine:
            jobs_for_each_engine[primary_template_type] = []

        jobs_for_each_engine[primary_template_type].append(target)

    count = 0
    for template_type in jobs_for_each_engine.keys():
        engine = plugins.ENGINES.get_engine(
            template_type,
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
                "Please specify a output file name for %s." % template
            )
        if config:
            result = {
                constants.LABEL_TEMPLATE: template,
                constants.LABEL_CONFIG: config,
                constants.LABEL_OUTPUT: output,
            }

        else:
            result = {output: template}
    return result


def handle_requires(requires):
    pypi_pkgs = []
    git_repos = []
    for require in requires:
        if isinstance(require, dict):
            require_type = require.get(constants.REQUIRE_TYPE, "")
            if require_type.upper() == constants.GIT_REQUIRE:
                git_repos.append(
                    GitRequire(
                        git_url=require.get(constants.GIT_URL),
                        branch=require.get(constants.GIT_BRANCH),
                        reference=require.get(constants.GIT_REFERENCE),
                        submodule=require.get(
                            constants.GIT_HAS_SUBMODULE, False
                        ),
                    )
                )
            elif require_type.upper() == constants.PYPI_REQUIRE:
                pypi_pkgs.append(require.get(constants.PYPI_PACKAGE_NAME))
        else:
            if is_repo(require):
                git_repos.append(GitRequire(require))
            else:
                pypi_pkgs.append(require)
    if pypi_pkgs:
        pip_install(pypi_pkgs)
        plugins.make_sure_all_pkg_are_loaded()
    if git_repos:
        git_clone(git_repos)


def is_repo(require):
    result = urlparse(require)
    return result.scheme != "" and result.netloc in KNOWN_DOMAIN_FOR_GIT
