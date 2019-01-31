class GitRequire(object):
    def __init__(self, git_url=None, branch=None, submodule=False):
        self.git_url = git_url
        self.submodule = submodule
        self.branch = branch

    def __eq__(self, other):
        return (
            self.git_url == other.git_url
            and self.submodule == other.submodule
            and self.branch == other.branch
        )

    def __repr__(self):
        return "%s,%s,%s" % (self.git_url, self.branch, self.submodule)
