from moban import constants
from moban.utils import handle_template
from moban.definitions import TemplateTarget


def parse_targets(options, targets):
    for target in targets:
        if constants.LABEL_OUTPUT in target:
            for template_target in handle_explicit_target(options, target):
                yield template_target
        else:
            for output, template_file in target.items():
                if isinstance(template_file, str) is False:
                    # grouping by template type feature
                    for template_target in handle_group_target(
                        options, template_file, output
                    ):
                        yield template_target
                else:
                    for template_target in handle_implicit_target(
                        options, template_file, output
                    ):
                        yield template_target


def handle_explicit_target(options, target):
    common_data_file = options[constants.LABEL_CONFIG]
    default_template_type = options[constants.LABEL_TEMPLATE_TYPE]
    template_file = target.get(
        constants.LABEL_TEMPLATE, options.get(constants.LABEL_TEMPLATE, None)
    )
    data_file = target.get(constants.LABEL_CONFIG, common_data_file)
    output = target[constants.LABEL_OUTPUT]
    template_type = target.get(constants.LABEL_TEMPLATE_TYPE)
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


def handle_group_target(options, template_file, output):
    # grouping by template type feature
    common_data_file = options[constants.LABEL_CONFIG]
    group_template_type = output
    for _output, _template_file in iterate_list_of_dicts(template_file):
        for src, dest, t_type in handle_template(
            _template_file, _output, options[constants.LABEL_TMPL_DIRS]
        ):
            yield TemplateTarget(
                src, common_data_file, dest, group_template_type
            )


def handle_implicit_target(options, template_file, output):
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


def iterate_list_of_dicts(list_of_dict):
    for adict in list_of_dict:
        for key, value in adict.items():
            yield (key, value)
