import os
import re
import sys
import stat
import errno
import logging

from moban import reporter, constants, exceptions
from moban.definitions import TemplateTarget

log = logging.getLogger(__name__)


def merge(left, right):
    """
    deep merge dictionary on the left with the one
    on the right.

    Fill in left dictionary with right one where
    the value of the key from the right one in
    the left one is missing or None.
    """
    if isinstance(left, dict) and isinstance(right, dict):
        for key, value in right.items():
            if key not in left:
                left[key] = value
            elif left[key] is None:
                left[key] = value
            else:
                left[key] = merge(left[key], value)
    return left


def search_file(base_dir, file_name):
    the_file = file_name
    if not os.path.exists(the_file):
        if base_dir:
            the_file = os.path.join(base_dir, file_name)
            if not os.path.exists(the_file):
                raise IOError(
                    constants.ERROR_DATA_FILE_NOT_FOUND % (file_name, the_file)
                )
        else:
            raise IOError(constants.ERROR_DATA_FILE_ABSENT % the_file)
    return the_file


def parse_targets(options, targets):
    common_data_file = options[constants.LABEL_CONFIG]
    default_template_type = options[constants.LABEL_TEMPLATE_TYPE]
    for target in targets:
        if constants.LABEL_OUTPUT in target:
            template_file = target.get(
                constants.LABEL_TEMPLATE,
                options.get(constants.LABEL_TEMPLATE, None),
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
        else:
            for output, template_file in target.items():
                for src, dest, t_type in handle_template(
                    template_file, output, options[constants.LABEL_TMPL_DIRS]
                ):
                    if t_type:
                        yield TemplateTarget(
                            src, common_data_file, dest, t_type
                        )
                    else:
                        yield TemplateTarget(
                            src, common_data_file, dest, default_template_type
                        )


def get_template_type(template_file):
    _, extension = os.path.splitext(template_file)
    if extension:
        template_type = extension[1:]
    else:
        template_type = None
    return template_type


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
                for a_triple in listing_directory_files_recusively(
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
    elif os.path.isdir(template_file_on_disk):
        for a_triple in list_dir_files(
            template_file, template_file_on_disk, output
        ):
            yield a_triple
    else:
        template_type = get_template_type(template_file)
        yield (template_file, output, template_type)


def find_file_in_template_dirs(src, template_dirs):
    log.debug(template_dirs)
    for folder in template_dirs:
        path = os.path.join(folder, src)
        if os.path.exists(path):
            return path
    else:
        return None


def list_dir_files(source, actual_source_path, dest):
    for file_name in os.listdir(actual_source_path):
        real_src_file = os.path.join(actual_source_path, file_name)
        if os.path.isfile(real_src_file):
            src_file_under_dir = os.path.join(source, file_name)
            dest_file_under_dir = os.path.join(dest, file_name)
            template_type = get_template_type(src_file_under_dir)
            yield (src_file_under_dir, dest_file_under_dir, template_type)


def listing_directory_files_recusively(source, actual_source_path, dest):
    for file_name in os.listdir(actual_source_path):
        src_file_under_dir = os.path.join(source, file_name)
        dest_file_under_dir = os.path.join(dest, file_name)
        real_src_file = os.path.join(actual_source_path, file_name)
        if os.path.isfile(real_src_file):
            template_type = get_template_type(src_file_under_dir)
            yield (src_file_under_dir, dest_file_under_dir, template_type)
        elif os.path.isdir(real_src_file):
            for a_triple in listing_directory_files_recusively(
                src_file_under_dir, real_src_file, dest_file_under_dir
            ):
                yield a_triple


def file_permissions_copy(source, dest):
    source_permissions = file_permissions(source)
    dest_permissions = file_permissions(dest)

    if source_permissions != dest_permissions:
        os.chmod(dest, source_permissions)


def file_permissions(afile):
    if sys.platform == "win32":
        return "no-permission-support"
    if not os.path.exists(afile):
        raise exceptions.FileNotFound(afile)
    return stat.S_IMODE(os.stat(afile).st_mode)


def strip_off_trailing_new_lines(content):
    return re.sub(r"(\n\s+)+$", r"\n", content)


def write_file_out(filename, content, strip=True, encode=True):
    dest_folder = os.path.dirname(filename)
    if dest_folder:
        mkdir_p(dest_folder)
    with open(filename, "wb") as out:
        if strip:
            content = strip_off_trailing_new_lines(content)
        if encode:
            content = content.encode("utf-8")
        out.write(content)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def pip_install(packages):
    import subprocess

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", " ".join(packages)]
    )


def git_clone(requires):
    from git import Repo

    moban_home = get_moban_home()
    mkdir_p(moban_home)

    for require in requires:
        repo_name = get_repo_name(require.git_url)
        local_repo_folder = os.path.join(moban_home, repo_name)
        if os.path.exists(local_repo_folder):
            reporter.report_git_pull(repo_name)
            repo = Repo(local_repo_folder)
            repo.git.pull()
            if require.submodule:
                reporter.report_info_message("updating submodule")
                repo.git.submodule("update")
        else:
            reporter.report_git_clone(require.git_url)
            repo = Repo.clone_from(
                require.git_url, local_repo_folder, **require.clone_params()
            )
            if require.submodule:
                reporter.report_info_message("checking out submodule")
                repo.git.submodule("update", "--init")


def get_template_path(template_dirs, template):
    temp_dir = ""

    for a_dir in template_dirs:
        template_file_exists = os.path.exists(
            os.path.join(a_dir, template)
        ) and os.path.isfile(os.path.join(a_dir, template))

        if template_file_exists:
            temp_dir = a_dir
            temp_file_path = os.path.join(
                os.getcwd(), os.path.join(temp_dir, template)
            )
            return temp_file_path
    raise exceptions.FileNotFound


def get_repo_name(repo_url):
    import giturlparse
    from giturlparse.parser import ParserError

    try:
        repo = giturlparse.parse(repo_url)
        return repo.name
    except ParserError:
        reporter.report_error_message(
            constants.MESSAGE_INVALID_GIT_URL % repo_url
        )
        raise


def get_moban_home():
    from appdirs import user_cache_dir

    home_dir = user_cache_dir(appname=constants.PROGRAM_NAME)
    return os.path.join(home_dir, constants.MOBAN_REPOS_DIR_NAME)


def verify_the_existence_of_directories(dirs):
    if not isinstance(dirs, list):
        dirs = [dirs]

    for directory in dirs:
        if os.path.exists(directory):
            continue
        should_I_ignore = (
            constants.DEFAULT_CONFIGURATION_DIRNAME in directory
            or constants.DEFAULT_TEMPLATE_DIRNAME in directory
        )
        if should_I_ignore:
            # ignore
            pass
        else:
            raise exceptions.DirectoryNotFound(
                constants.MESSAGE_DIR_NOT_EXIST % os.path.abspath(directory)
            )
