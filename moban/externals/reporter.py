import sys

import crayons

import moban.constants as constants

MESSAGE_TEMPLATING = "{0} {1} to {2}"
MESSAGE_UP_TO_DATE = "Everything is up to date!"
MESSAGE_NO_TEMPLATING = "No actions performed"
MESSAGE_REPORT = "{0} {1} out of {2} files."
MESSAGE_TEMPLATED_ALL = "{0} {1} files."
MESSAGE_PULLING_REPO = "Updating {0}..."
MESSAGE_CLONING_REPO = "Cloning {0}..."
MESSAGE_TEMPLATE_NOT_IN_MOBAN_FILE = "{0} is not defined in your moban file!"
MESSAGE_FILE_EXTENSION_NOT_NEEDED = "File extension is not required for ad-hoc\
 type"

GLOBAL = {"PRINT": True}


def report_templating(
    action_in_present_continuous_tense, source_file, destination_file
):
    if destination_file:
        do_print(
            MESSAGE_TEMPLATING.format(
                action_in_present_continuous_tense,
                crayons.yellow(source_file),
                crayons.green(destination_file),
            )
        )
    else:
        do_print(
            f"{action_in_present_continuous_tense} {crayons.yellow(source_file)}"
        )


def report_no_action():
    do_print(crayons.yellow(MESSAGE_NO_TEMPLATING, bold=True))


def report_full_run(action_in_past_tense, file_count):
    figure = crayons.green(str(file_count), bold=True)
    message = MESSAGE_TEMPLATED_ALL.format(action_in_past_tense, figure)
    do_print(_format_single(message, file_count))


def report_partial_run(action_in_past_tense, file_count, total):
    figure = crayons.green(str(file_count), bold=True)
    total_figure = crayons.yellow(str(total), bold=True)
    message = MESSAGE_REPORT.format(action_in_past_tense, figure, total_figure)
    do_print(_format_single(message, total))


def report_error_message(message):
    error_print(crayons.white("Error: ", bold=True) + crayons.red(message))


def report_warning_message(message):
    error_print(
        crayons.white("Warning: ", bold=True) + crayons.yellow(message)
    )


def report_info_message(message):
    do_print(crayons.white("Info: ") + crayons.green(message))


def report_up_to_date():
    do_print(crayons.green(MESSAGE_UP_TO_DATE, bold=True))


def convert_to_shell_exit_code(number_of_templated_files):
    return (
        constants.HAS_CHANGES
        if number_of_templated_files > 0
        else constants.NO_CHANGES
    )


def report_git_pull(repo):
    colored_repo = crayons.green(repo, bold=True)
    do_print(MESSAGE_PULLING_REPO.format(colored_repo))


def report_git_clone(repo):
    colored_repo = crayons.green(repo, bold=True)
    do_print(MESSAGE_CLONING_REPO.format(colored_repo))


def report_template_not_in_moban_file(template):
    message = MESSAGE_TEMPLATE_NOT_IN_MOBAN_FILE.format(template)
    report_warning_message(message)


def _format_single(message, count):
    if count == 1:
        return message.replace("files", "file")
    return message


def report_file_extension_not_needed():
    report_info_message(MESSAGE_FILE_EXTENSION_NOT_NEEDED)


def do_print(message):
    if GLOBAL["PRINT"]:
        print(message)


def error_print(message):
    sys.stderr.write(message + "\n")
