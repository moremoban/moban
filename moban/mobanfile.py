import moban.constants as constants
from moban.engine import EngineFactory
from moban.utils import merge, parse_targets


def handle_moban_file_v1(moban_file_configurations, command_line_options):
    merged_options = None
    if constants.LABEL_CONFIG in moban_file_configurations:
        merged_options = merge(
            command_line_options,
            moban_file_configurations[constants.LABEL_CONFIG])
    merged_options = merge(
        command_line_options,
        constants.DEFAULT_OPTIONS)
    list_of_templating_parameters = parse_targets(
        merged_options,
        moban_file_configurations[constants.LABEL_TARGETS])
    engine_class = EngineFactory.get_engine(
        merged_options[constants.LABEL_TEMPLATE_TYPE])
    engine = engine_class(
        merged_options[constants.LABEL_TMPL_DIRS],
        merged_options[constants.LABEL_CONFIG_DIR])
    engine.render_to_files(list_of_templating_parameters)
    engine.report()
