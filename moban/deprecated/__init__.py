import sys
from functools import wraps

from moban import reporter, constants, file_system
from moban.deprecated import repo
from moban.deprecated.library import LIBRARIES


def deprecated(message):
    def tags_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwds):
            reporter.report_warning_message(message)
            return func(*args, **kwds)

        return func_wrapper

    return tags_decorator


class GitRequire(object):
    def __init__(
        self, git_url=None, branch=None, submodule=False, reference=None
    ):
        self.git_url = git_url
        self.submodule = submodule
        self.branch = branch
        self.reference = reference

    def clone_params(self):
        clone_params = {
            "single_branch": True,
            "depth": constants.DEFAULT_CLONE_DEPTH,
        }
        if self.branch is not None:
            clone_params["branch"] = self.branch
        elif self.reference is not None:
            clone_params["reference"] = self.reference
        return clone_params

    def __eq__(self, other):
        return (
            self.git_url == other.git_url
            and self.submodule == other.submodule
            and self.branch == other.branch
            and self.reference == other.reference
        )

    def __repr__(self):
        return "%s,%s,%s" % (self.git_url, self.branch, self.submodule)


def pip_install(packages):
    import subprocess

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", " ".join(packages)]
    )


@deprecated(constants.MESSAGE_DEPRECATE_MOBAN_NOTATION_SINCE_0_6_0)
def deprecated_moban_path_notation(directory):
    translated_directory = None
    library_or_repo_name, relative_path = directory.split(":")
    potential_repo_path = file_system.path_join(
        repo.get_moban_home(), library_or_repo_name
    )
    if file_system.exists(potential_repo_path):
        # expand repo template path
        if relative_path:
            translated_directory = file_system.path_join(
                potential_repo_path, relative_path
            )
        else:
            translated_directory = potential_repo_path
    else:
        # expand pypi template path
        library_path = LIBRARIES.resource_path_of(library_or_repo_name)
        if relative_path:
            translated_directory = file_system.path_join(
                library_path, relative_path
            )
        else:
            translated_directory = library_path
    return translated_directory
