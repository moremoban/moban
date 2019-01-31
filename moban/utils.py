import os
import re
import sys
import stat
import errno

import moban.reporter as reporter
import moban.constants as constants
import moban.exceptions as exceptions


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
    for target in targets:
        if constants.LABEL_OUTPUT in target:
            template_file = target.get(
                constants.LABEL_TEMPLATE,
                options.get(constants.LABEL_TEMPLATE, None),
            )
            data_file = target.get(constants.LABEL_CONFIG, common_data_file)
            output = target[constants.LABEL_OUTPUT]
            yield ((template_file, data_file, output))
        else:
            for output, template_file in target.items():
                yield ((template_file, common_data_file, output))


def expand_directories(file_list, template_dirs):
    for template_file, data_file, output in file_list:
        true_template_file = template_file
        for a_template_dir in template_dirs:
            true_template_file = os.path.join(a_template_dir, template_file)
            if os.path.exists(true_template_file):
                break
        if os.path.isdir(true_template_file):
            for file_name in os.listdir(true_template_file):
                template_file = "/".join([template_file, file_name])
                template_file = template_file.replace("\\", "/")
                base_output_name, _ = os.path.splitext(file_name)
                yield (
                    (
                        template_file,
                        data_file,
                        os.path.join(output, base_output_name),
                    )
                )
        else:
            yield ((template_file, data_file, output))


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


def _remove_dot_git(repo_name):
    return repo_name.split(".")[0]
