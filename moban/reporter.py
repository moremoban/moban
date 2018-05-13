import crayons

import moban.constants as constants

MESSAGE_TEMPLATING = "Templating {0} to {1}"
MESSAGE_NO_ACTION = "Everything is up to date!"
MESSAGE_REPORT = "Templated {0} out of {1} files."
MESSAGE_TEMPLATED_ALL = "Templated {0} files."


def report_templating(source_file, destination_file):
    print(
        MESSAGE_TEMPLATING.format(
            crayons.yellow(source_file), crayons.green(destination_file)
        )
    )


def report_no_action():
    print(crayons.green(MESSAGE_NO_ACTION, bold=True))


def report_full_run(file_count):
    figure = crayons.green(str(file_count), bold=True)
    print(MESSAGE_TEMPLATED_ALL.format(figure))


def report_partial_run(file_count, total):
    figure = crayons.green(str(file_count), bold=True)
    total_figure = crayons.yellow(str(total), bold=True)
    print(MESSAGE_REPORT.format(figure, total_figure))


def report_error_message(message):
    print(crayons.white("Error: ", bold=True) + crayons.red(message))


def convert_to_shell_exit_code(number_of_templated_files):
    return (
        constants.HAS_CHANGES
        if number_of_templated_files > 0
        else constants.NO_CHANGES
    )
