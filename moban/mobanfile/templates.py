import logging

from moban import reporter, file_system

LOG = logging.getLogger(__name__)


def handle_template(template_file, output, template_dirs):
    LOG.info("handling %s" % template_file)

    template_file = file_system.to_unicode(template_file)
    multi_fs = file_system.get_multi_fs(template_dirs)
    if template_file.endswith("**"):
        source_dir = template_file[:-3]
        _, fs = multi_fs.which(source_dir)
        if fs:
            for a_triple in _listing_directory_files_recusively(
                fs, source_dir, output
            ):
                yield a_triple
        else:
            reporter.report_error_message(
                "{0} cannot be found".format(template_file)
            )
    else:
        _, fs = multi_fs.which(template_file)
        if fs is None:
            reporter.report_error_message(
                "{0} cannot be found".format(template_file)
            )
        elif fs.isdir(template_file):
            for a_triple in _list_dir_files(fs, template_file, output):
                yield a_triple
        else:
            template_type = _get_template_type(template_file)
            yield (template_file, output, template_type)


def _list_dir_files(fs, source, dest):
    for file_name in fs.listdir(source):
        # please note jinja2 does NOT like windows path
        # hence the following statement looks like cross platform
        #  src_file_under_dir = os.path.join(source, file_name)
        # but actually it breaks windows instead.
        src_file_under_dir = "%s/%s" % (source, file_name)
        if fs.isfile(src_file_under_dir):
            dest_file_under_dir = dest + "/" + file_name
            template_type = _get_template_type(src_file_under_dir)
            yield (src_file_under_dir, dest_file_under_dir, template_type)


def _listing_directory_files_recusively(fs, source, dest):
    for file_name in fs.listdir(source):
        src_file_under_dir = source + "/" + file_name
        dest_file_under_dir = dest + "/" + file_name
        if fs.isfile(src_file_under_dir):
            template_type = _get_template_type(src_file_under_dir)
            yield (src_file_under_dir, dest_file_under_dir, template_type)
        elif fs.isdir(src_file_under_dir):
            for a_triple in _listing_directory_files_recusively(
                fs, src_file_under_dir, dest_file_under_dir
            ):
                yield a_triple


def _get_template_type(template_file):
    _, extension = file_system.path_splitext(template_file)
    if extension:
        template_type = extension[1:]
    else:
        template_type = None
    return template_type
