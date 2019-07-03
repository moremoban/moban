import os
import sys
import subprocess

from moban import reporter, constants, exceptions
from moban.utils import mkdir_p


def git_clone(requires):
    from git import Repo

    if sys.platform != "win32":
        # Unfortunately for windows user, the following function
        # needs shell=True, which expose security risk. I would
        # rather not to trade it with its marginal benefit
        make_sure_git_is_available()

    moban_home = get_moban_home()
    mkdir_p(moban_home)

    for require in requires:
        repo_name = get_repo_name(require.git_url)
        local_repo_folder = os.path.join(moban_home, repo_name)
        if os.path.exists(local_repo_folder):
            reporter.report_git_pull(repo_name)
            repo = Repo(local_repo_folder)
            repo.git.pull()
            if require.reference:
                repo.git.checkout(require.reference)
            elif require.branch:
                repo.git.checkout(require.branch)
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


def get_repo_name(repo_url):
    import giturlparse

    try:
        repo = giturlparse.parse(repo_url)
        name = repo.repo
        if name.endswith("/"):
            name = name[:-1]
        return name
    except AttributeError:
        reporter.report_error_message(
            constants.MESSAGE_INVALID_GIT_URL % repo_url
        )
        raise


def get_moban_home():
    from appdirs import user_cache_dir

    home_dir = user_cache_dir(appname=constants.PROGRAM_NAME)
    return os.path.join(home_dir, constants.MOBAN_REPOS_DIR_NAME)


def make_sure_git_is_available():
    try:
        subprocess.check_output(["git", "--help"])
    except Exception:
        raise exceptions.NoGitCommand("Please install git command")
