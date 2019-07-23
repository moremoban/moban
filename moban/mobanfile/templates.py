import logging

from moban import reporter
from moban import file_system as moban_fs
from moban.utils import find_file_in_template_dirs

import fs
import fs.path

log = logging.getLogger(__name__)


def handle_template(template_file, output, template_dirs):
    log.info("handling %s" % template_file)
    template_file_on_disk = find_file_in_template_dirs(
        template_file, template_dirs
    )
    if template_file_on_disk is None:
        if template_file.endswith("**"):
            source_dir = template_file[:-3]
            src_path = find_file_in_template_dirs(source_dir, template_dirs)
            if src_path:
                for a_triple in _listing_directory_files_recusively(
                    source_dir, src_path, output
                ):
                    yield a_triple
            else:
                reporter.report_error_message(
                    "{0} cannot be found".format(template_file)
                )
        else:
            reporter.report_error_message(
                "{0} cannot be found".format(template_file)
            )
    elif moban_fs.is_dir(template_file_on_disk):
        for a_triple in _list_dir_files(
            template_file, template_file_on_disk, output
        ):
            yield a_triple
    else:
        template_type = _get_template_type(template_file)
        yield (template_file, output, template_type)


def _list_dir_files(source, actual_source_path, dest):
    for file_name in moban_fs.list_dir(actual_source_path):
        if moban_fs.is_file(fs.path.join(actual_source_path, file_name)):
            # please note jinja2 does NOT like windows path
            # hence the following statement looks like cross platform
            #  src_file_under_dir = os.path.join(source, file_name)
            # but actually it breaks windows instead.
            src_file_under_dir = "%s/%s" % (source, file_name)

            dest_file_under_dir = fs.path.join(dest, file_name)
            template_type = _get_template_type(src_file_under_dir)
            yield (src_file_under_dir, dest_file_under_dir, template_type)


def _listing_directory_files_recusively(source, actual_source_path, dest):
    for file_name in moban_fs.list_dir(actual_source_path):
        src_file_under_dir = fs.path.join(source, file_name)
        dest_file_under_dir = fs.path.join(dest, file_name)
        real_src_file = fs.path.join(actual_source_path, file_name)
        if moban_fs.is_file(fs.path.join(actual_source_path, file_name)):
            template_type = _get_template_type(src_file_under_dir)
            yield (src_file_under_dir, dest_file_under_dir, template_type)
        elif moban_fs.is_dir(fs.path.join(actual_source_path, file_name)):
            for a_triple in _listing_directory_files_recusively(
                src_file_under_dir, real_src_file, dest_file_under_dir
            ):
                yield a_triple


def _get_template_type(template_file):
    _, extension = fs.path.splitext(template_file)
    if extension:
        template_type = extension[1:]
    else:
        template_type = None
    return template_type
