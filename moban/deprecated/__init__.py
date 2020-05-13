import sys
from functools import wraps

from moban import constants
from moban.core import plugins
from moban.externals import reporter, file_system
from moban.deprecated import repo
from moban.deprecated.repo import git_clone
from moban.deprecated.library import LIBRARIES

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


KNOWN_DOMAIN_FOR_GIT = ["github.com", "gitlab.com", "bitbucket.com"]


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
        [sys.executable, "-m", "pip", "install", " ".join(packages)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
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


@deprecated(constants.MESSAGE_DEPRECATE_REQUIRES_SINCE_0_6_0)
def handle_requires(requires):
    pypi_pkgs = []
    git_repos = []
    for require in requires:
        if isinstance(require, dict):
            require_type = require.get(constants.REQUIRE_TYPE, "")
            if require_type.upper() == constants.GIT_REQUIRE:
                git_require = GitRequire(
                    git_url=require.get(constants.GIT_URL),
                    branch=require.get(constants.GIT_BRANCH),
                    reference=require.get(constants.GIT_REFERENCE),
                    submodule=require.get(constants.GIT_HAS_SUBMODULE, False),
                )

                git_repos.append(git_require)
            elif require_type.upper() == constants.PYPI_REQUIRE:
                pypi_pkgs.append(require.get(constants.PYPI_PACKAGE_NAME))
        else:
            if is_repo(require):
                git_repos.append(GitRequire(require))
            else:
                pypi_pkgs.append(require)
    if pypi_pkgs:
        pip_install(pypi_pkgs)
        plugins.make_sure_all_pkg_are_loaded()
    if git_repos:
        git_clone(git_repos)


def is_repo(require):
    result = urlparse(require)
    return result.scheme != "" and result.netloc in KNOWN_DOMAIN_FOR_GIT


@deprecated(constants.MESSAGE_DEPRECATE_COPY_SINCE_0_4_0)
def handle_copy(merged_options, copy_config):
    copy_targets = []
    for (dest, src) in _iterate_list_of_dicts(copy_config):
        copy_targets.append(
            {
                constants.LABEL_TEMPLATE: src,
                constants.LABEL_OUTPUT: dest,
                constants.LABEL_TEMPLATE_TYPE: constants.TEMPLATE_COPY,
            }
        )
    return copy_targets


def _iterate_list_of_dicts(list_of_dict):
    for adict in list_of_dict:
        for key, value in adict.items():
            yield (key, value)
