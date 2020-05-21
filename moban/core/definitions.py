import logging

from moban import constants

LOG = logging.getLogger(__name__)


class TemplateTarget(object):
    def __init__(
        self,
        template_file,
        data_file,
        output,
        template_type=constants.DEFAULT_TEMPLATE_TYPE,
    ):
        self.template_file = template_file
        self.data_file = data_file
        self.original_output = output
        self.template_type = template_type
        self.output = self.original_output

        self.set_template_type(template_type)
        LOG.info("create a target {}".format(self))

    def set_template_type(self, new_template_type):
        self.template_type = new_template_type
        if self.original_output.endswith(self.template_type):
            self.output = self.original_output.replace(
                "." + self.template_type, ""
            )
        else:
            self.output = self.original_output

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
