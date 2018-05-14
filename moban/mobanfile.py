import os
import moban.constants as constants
import moban.reporter as reporter
from moban.engine import EngineFactory
from moban.utils import merge, parse_targets
from moban.copier import Copier


def find_default_moban_file():
    for moban_file in constants.DEFAULT_MOBAN_FILES:
        if os.path.exists(moban_file):
            break
    else:
        moban_file = None
    return moban_file


def handle_copy(template_dirs, copy_config):
    copier = Copier(template_dirs)
    copier.copy_files(copy_config)
    copier.report()
    return copier.number_of_copied_files()


def handle_moban_file_v1(moban_file_configurations, command_line_options):
    merged_options = None
    if constants.LABEL_CONFIG in moban_file_configurations:
        merged_options = merge(
            command_line_options,
            moban_file_configurations[constants.LABEL_CONFIG],
        )
    merged_options = merge(command_line_options, constants.DEFAULT_OPTIONS)
    list_of_templating_parameters = parse_targets(
        merged_options, moban_file_configurations[constants.LABEL_TARGETS]
    )
    engine_class = EngineFactory.get_engine(
        merged_options[constants.LABEL_TEMPLATE_TYPE]
    )
    engine = engine_class(
        merged_options[constants.LABEL_TMPL_DIRS],
        merged_options[constants.LABEL_CONFIG_DIR],
    )
    engine.render_to_files(list_of_templating_parameters)
    engine.report()
    number_of_copied_files = handle_copy(
        merged_options[constants.LABEL_TMPL_DIRS],
        moban_file_configurations[constants.LABEL_COPY]
        )
    exit_code = reporter.convert_to_shell_exit_code(
        engine.number_of_templated_files() + number_of_copied_files
    )
    reporter.report_up_to_date()
    return exit_code
