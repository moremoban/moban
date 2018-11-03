import crayons
import moban.constants as constants

MESSAGE_TEMPLATING = "Templating {0} to {1}"
MESSAGE_COPYING = "Copying {0} to {1}"
MESSAGE_UP_TO_DATE = "Everything is up to date!"
MESSAGE_NO_COPY = "No copying"
MESSAGE_NO_TEMPLATING = "No templating"
MESSAGE_REPORT = "Templated {0} out of {1} files."
MESSAGE_TEMPLATED_ALL = "Templated {0} files."
MESSAGE_COPY_REPORT = "Copied {0} out of {1} files."
MESSAGE_COPIED_ALL = "Copied {0} files."
MESSAGE_PULLING_REPO = "Updating {0}..."
MESSAGE_CLONING_REPO = "Cloning {0}..."


def report_templating(source_file, destination_file):
    print(
        MESSAGE_TEMPLATING.format(
            crayons.yellow(source_file), crayons.green(destination_file)
        )
    )


def report_no_action():
    print(crayons.yellow(MESSAGE_NO_TEMPLATING, bold=True))


def report_no_copying():
    print(crayons.yellow(MESSAGE_NO_COPY, bold=True))


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


def report_up_to_date():
    print(crayons.green(MESSAGE_UP_TO_DATE, bold=True))


def convert_to_shell_exit_code(number_of_templated_files):
    return (
        constants.HAS_CHANGES
        if number_of_templated_files > 0
        else constants.NO_CHANGES
    )


def report_copying(source_file, destination_file):
    print(
        MESSAGE_COPYING.format(
            crayons.yellow(source_file), crayons.green(destination_file)
        )
    )


def report_copying_summary(total, copies):
    if total == copies:
        figure = crayons.green(str(total), bold=True)
        message = MESSAGE_COPIED_ALL.format(figure)
        print(_format_single(message, total))
    else:
        figure = crayons.green(str(copies), bold=True)
        total_figure = crayons.yellow(str(total), bold=True)
        message = MESSAGE_COPY_REPORT.format(figure, total_figure)
        print(_format_single(message, total))


def report_git_pull(repo):
    colored_repo = crayons.green(repo, bold=True)
    print(MESSAGE_PULLING_REPO.format(colored_repo))


def report_git_clone(repo):
    colored_repo = crayons.green(repo, bold=True)
    print(MESSAGE_CLONING_REPO.format(colored_repo))


def _format_single(message, count):
    if count == 1:
        return message.replace("files", "file")
    return message
