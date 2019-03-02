import os

from moban import constants


class GitRequire(object):
    def __init__(self, git_url=None, branch=None, submodule=False):
        self.git_url = git_url
        self.submodule = submodule
        self.branch = branch

    def clone_params(self):
        clone_params = {
            "single_branch": True,
            "depth": constants.DEFAULT_CLONE_DEPTH,
        }
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


class TemplateTarget(object):
    def __init__(
        self,
        template_file,
        data_file,
        output,
        template_type=constants.DEFAULT_TEMPLATE_TYPE,
        needs_ad_hoc=False,
    ):
        self.template_file = template_file
        self.data_file = data_file
        self.original_output = output
        self.template_type = template_type
        self.output = self.original_output
        self.needs_ad_hoc = needs_ad_hoc

        if needs_ad_hoc:
            self.set_template_parameters(template_type)
        else:
            self.set_template_type(template_type)

    def set_template_type(self, new_template_type):
        self.template_type = new_template_type
        if self.original_output.endswith(self.template_type):
            self.output, _ = os.path.splitext(self.original_output)
        else:
            self.output = self.original_output

    def set_template_parameters(self, template_type):
        template_parameters = self.template_type
        self.template_type = {}
        self.template_type[constants.TEMPLATE_TYPES_BASE_TYPE] = (
            template_parameters[0][constants.TEMPLATE_TYPES_BASE_TYPE])
        self.template_type[constants.TEMPLATE_TYPES_OPTIONS] = (
            template_parameters[1][constants.TEMPLATE_TYPES_OPTIONS])

    def __eq__(self, other):
        return (
            self.template_file == other.template_file
            and self.data_file == other.data_file
            and self.output == other.output
            and self.template_type == self.template_type
        )

    def __repr__(self):
        return "%s,%s,%s,%s" % (
            self.template_file,
            self.data_file,
            self.output,
            self.template_type,
        )
