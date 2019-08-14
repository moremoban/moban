import sys
from functools import wraps

from moban import reporter, constants


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
