from lml.plugin import PluginInfo

from moban import constants


@PluginInfo(constants.TEMPLATE_ENGINE_EXTENSION, tags=["strip"])
class StripEngine(object):
    """
    Works like 'copy', but strip empty spaces before and after
    """

    ACTION_IN_PRESENT_CONTINUOUS_TENSE = "Stripping"
    ACTION_IN_PAST_TENSE = "Stripped"

    def __init__(self, template_fs, extensions=None):
        self.template_fs = template_fs

    def get_template(self, template_file):
        return self.template_fs.readbytes(template_file).strip()

    def get_template_from_string(self, string):
        return string.strip()

    def apply_template(self, template, *_):
        return template
