import uuid
import logging

from moban import core, constants, exceptions
from moban.externals import reporter
from moban.core.definitions import TemplateTarget
from .store import STORE
from .templates import handle_template

LOG = logging.getLogger(__name__)


def extract_target(options):
    template, config, output = (
        options.get(constants.LABEL_TEMPLATE),
        options.get(constants.LABEL_CONFIG),
        options.get(constants.LABEL_OUTPUT),
    )
    result = []
    if template:
        if output is None:
            raise Exception(
                f"Please specify a output file name for {template}"
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


def extract_group_targets(group, targets):
    for target in targets:
        if constants.LABEL_OUTPUT in target:
            continue

        for group_name, group_targets in target.items():
            if isinstance(group_targets, str) is False and group_name == group:
                # grouping by template type feature
                return [{group_name: group_targets}]
    raise exceptions.GroupTargetNotFound(f"{group} is not found")


def parse_targets(options, targets):
    LOG.info("paring targets..")
    STORE.init()
    for target in targets:
        if constants.LABEL_OUTPUT in target:
            for template_target in _handle_explicit_target(options, target):
                STORE.add(template_target)
        else:
            for output, template_file in target.items():
                if isinstance(template_file, str):
                    for template_target in _handle_implicit_target(
                        options, template_file, output
                    ):
                        STORE.add(template_target)
                else:
                    # grouping by template type feature
                    group_template_type = output
                    a_list_short_hand_targets = template_file
                    for template_target in _handle_group_target(
                        options, a_list_short_hand_targets, group_template_type
                    ):
                        STORE.add(template_target)


def _handle_explicit_target(options, target):
    common_data_file = options[constants.LABEL_CONFIG]
    default_template_type = options[constants.LABEL_TEMPLATE_TYPE]
    template_file = target.get(
        constants.LABEL_TEMPLATE, options.get(constants.LABEL_TEMPLATE, None)
    )
    data_file = target.get(constants.LABEL_CONFIG, common_data_file)
    output = target[constants.LABEL_OUTPUT]
    if output:
        template_type = target.get(constants.LABEL_TEMPLATE_TYPE)
    else:
        template_type = constants.TEMPLATE_DELETE
    if template_type and len(template_type) > 0:
        if constants.TEMPLATE_TYPES_FILE_EXTENSIONS in template_type:
            reporter.report_file_extension_not_needed()
        if constants.TEMPLATE_TYPES_BASE_TYPE in template_type:
            adhoc_type = uuid.uuid4().hex
            file_extension = uuid.uuid4().hex
            base_type = template_type[constants.TEMPLATE_TYPES_BASE_TYPE]
            template_types_options = template_type[
                constants.TEMPLATE_TYPES_OPTIONS
            ]
            the_adhoc_type = {
                adhoc_type: {
                    constants.TEMPLATE_TYPES_FILE_EXTENSIONS: [file_extension],
                    constants.TEMPLATE_TYPES_BASE_TYPE: base_type,
                    constants.TEMPLATE_TYPES_OPTIONS: template_types_options,
                }
            }
            core.ENGINES.register_options(the_adhoc_type)
            template_type = file_extension
    for src, dest, t_type in handle_template(
        template_file, output, options[constants.LABEL_TMPL_DIRS]
    ):
        if template_type:
            yield TemplateTarget(src, data_file, dest, template_type)
        else:
            if t_type:
                yield TemplateTarget(src, data_file, dest, t_type)
            else:
                yield TemplateTarget(
                    src, data_file, dest, default_template_type
                )


def _handle_group_target(
    options, a_list_short_hand_targets, group_template_type
):
    # grouping by template type feature
    common_data_file = options[constants.LABEL_CONFIG]
    for _output, _template_file in _iterate_list_of_dicts(
        a_list_short_hand_targets
    ):
        for src, dest, t_type in handle_template(
            _template_file, _output, options[constants.LABEL_TMPL_DIRS]
        ):
            yield TemplateTarget(
                src, common_data_file, dest, group_template_type
            )


def _handle_implicit_target(options, template_file, output):
    common_data_file = options[constants.LABEL_CONFIG]
    default_template_type = options[constants.LABEL_TEMPLATE_TYPE]
    for src, dest, t_type in handle_template(
        template_file, output, options[constants.LABEL_TMPL_DIRS]
    ):
        if t_type:
            yield TemplateTarget(src, common_data_file, dest, t_type)
        else:
            yield TemplateTarget(
                src, common_data_file, dest, default_template_type
            )


def _iterate_list_of_dicts(list_of_dict):
    for adict in list_of_dict:
        for key, value in adict.items():
            yield (key, value)
