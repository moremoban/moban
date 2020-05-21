import logging

from moban import constants
from moban.externals import reporter, file_system
from .store import STORE

LOG = logging.getLogger(__name__)


def handle_template(template_file, output, template_dirs):
    LOG.info(f"handling {template_file}")

    template_file = template_file
    multi_fs = file_system.get_multi_fs(template_dirs)
    if template_file.endswith("**"):
        source_dir = template_file[:-3]
        _, fs = multi_fs.which(source_dir)
        if fs:
            yield from _listing_directory_files_recusively(
                fs, source_dir, output
            )
        else:
            reporter.report_error_message(f"{template_file} cannot be found")
    else:
        if STORE.look_up_by_output.get(template_file) is None:
            _, fs = multi_fs.which(template_file)
            if fs is None:
                reporter.report_error_message(
                    f"{template_file} cannot be found"
                )
            elif fs.isdir(template_file):
                yield from _list_dir_files(fs, template_file, output)
            else:
                yield _create_a_single_target(template_file, output)
        else:
            # when template_file is not found, it means
            it_is_generated_by_moban = template_file
            STORE.intermediate_targets.append(it_is_generated_by_moban)
            yield _create_a_single_target(template_file, output)


def _list_dir_files(fs, source, dest):
    for file_name in fs.listdir(source):
        # please note jinja2 does NOT like windows path
        # hence the following statement looks like cross platform
        #  src_file_under_dir = os.path.join(source, file_name)
        # but actually it breaks windows instead.
        src_file_under_dir = f"{source}/{file_name}"
        if fs.isfile(src_file_under_dir):
            dest_file_under_dir = f"{dest}/{file_name}"
            template_type = _get_template_type(src_file_under_dir)
            yield (src_file_under_dir, dest_file_under_dir, template_type)


def _listing_directory_files_recusively(fs, source, dest):
    for file_name in fs.listdir(source):
        src_file_under_dir = f"{source}/{file_name}"
        dest_file_under_dir = f"{dest}/{file_name}"
        if fs.isfile(src_file_under_dir):
            template_type = _get_template_type(src_file_under_dir)
            yield (src_file_under_dir, dest_file_under_dir, template_type)
        elif fs.isdir(src_file_under_dir):
            yield from _listing_directory_files_recusively(
                fs, src_file_under_dir, dest_file_under_dir
            )


def _create_a_single_target(template_file, output):
    if output == constants.TEMPLATE_DELETE + "!":
        template_type = constants.TEMPLATE_DELETE
    else:
        template_type = _get_template_type(template_file)
    # output.jj2: source.jj2 means 'copy'
    if template_type and output.endswith("." + template_type):
        LOG.info(
            f"template type switched to from {template_type} to "
            + constants.TEMPLATE_COPY
        )
        template_type = constants.TEMPLATE_COPY
    return (template_file, output, template_type)


def _get_template_type(template_file):
    _, extension = file_system.path_splitext(template_file)
    if extension:
        template_type = extension[1:]
    else:
        template_type = None
    return template_type
