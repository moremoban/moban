from moban import constants


class GitRequire(object):
    def __init__(self, git_url=None, branch=None, submodule=False):
        self.git_url = git_url
        self.submodule = submodule
        self.branch = branch

    def clone_params(self):
        clone_params = {"single_branch": True}
        if self.branch is not None:
            clone_params["branch"] = self.branch
        return clone_params

    def __eq__(self, other):
        return (
            self.git_url == other.git_url
            and self.submodule == other.submodule
            and self.branch == other.branch
        )

    def __repr__(self):
        return "%s,%s,%s" % (self.git_url, self.branch, self.submodule)


class Target(object):
    def __init__(self, type):
        self.type = type


class TemplateTarget(Target):
    def __init__(self, template_file, data_file, output):
        super(TemplateTarget, self).__init__(constants.ACTION_TEMPLATE)
        self.template_file = template_file
        self.data_file = data_file
        self.output = output


class CopyTarget(Target):
    def __init__(self, source, destination):
        super(CopyTarget, self).__init__(constants.ACTION_TEMPLATE)
        self.source = source
        self.destination = destination
