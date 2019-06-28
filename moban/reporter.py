import moban.constants as constants

import crayons

MESSAGE_TEMPLATING = "Templating {0} to {1}"
MESSAGE_UP_TO_DATE = "Everything is up to date!"
MESSAGE_NO_TEMPLATING = "No templating"
MESSAGE_REPORT = "Templated {0} out of {1} files."
MESSAGE_TEMPLATED_ALL = "Templated {0} files."
MESSAGE_PULLING_REPO = "Updating {0}..."
MESSAGE_CLONING_REPO = "Cloning {0}..."
MESSAGE_USING_ENV_VARS = "Attempting to use environment vars as data..."
MESSAGE_TEMPLATE_NOT_IN_MOBAN_FILE = "{0} is not defined in your moban file!"
MESSAGE_FILE_EXTENSION_NOT_NEEDED = "File extension is not required for ad-hoc\
 type"


def report_templating(source_file, destination_file):
    print(
        MESSAGE_TEMPLATING.format(
            crayons.yellow(source_file), crayons.green(destination_file)
        )
    )


def report_no_action():
    print(crayons.yellow(MESSAGE_NO_TEMPLATING, bold=True))


def report_full_run(file_count):
    figure = crayons.green(str(file_count), bold=True)
    message = MESSAGE_TEMPLATED_ALL.format(figure)
    print(_format_single(message, file_count))


def report_partial_run(file_count, total):
    figure = crayons.green(str(file_count), bold=True)
    total_figure = crayons.yellow(str(total), bold=True)
    message = MESSAGE_REPORT.format(figure, total_figure)
    print(_format_single(message, total))


def report_error_message(message):
    print(crayons.white("Error: ", bold=True) + crayons.red(message))


def report_warning_message(message):
    print(crayons.white("Warning: ", bold=True) + crayons.yellow(message))


def report_info_message(message):
    print(crayons.white("Info: ") + crayons.green(message))


def report_up_to_date():
    print(crayons.green(MESSAGE_UP_TO_DATE, bold=True))


def convert_to_shell_exit_code(number_of_templated_files):
    return (
        constants.HAS_CHANGES
        if number_of_templated_files > 0
        else constants.NO_CHANGES
    )


def report_git_pull(repo):
    colored_repo = crayons.green(repo, bold=True)
    print(MESSAGE_PULLING_REPO.format(colored_repo))


def report_git_clone(repo):
    colored_repo = crayons.green(repo, bold=True)
    print(MESSAGE_CLONING_REPO.format(colored_repo))


def report_using_env_vars():
    report_warning_message(MESSAGE_USING_ENV_VARS)


def report_template_not_in_moban_file(template):
    message = MESSAGE_TEMPLATE_NOT_IN_MOBAN_FILE.format(template)
    report_warning_message(message)


def _format_single(message, count):
    if count == 1:
        return message.replace("files", "file")
    return message


def report_file_extension_not_needed():
    report_info_message(MESSAGE_FILE_EXTENSION_NOT_NEEDED)
