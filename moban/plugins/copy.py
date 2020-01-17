from lml.plugin import PluginInfo

from moban import constants


@PluginInfo(
    constants.TEMPLATE_ENGINE_EXTENSION, tags=[constants.TEMPLATE_COPY]
)
class ContentForwardEngine(object):
    """
    Does no templating, works like 'copy'.

    Respects templating directories, for example: naughty.template
    could exist in any of template directires: dir1,
    dir2, dir3, and this engine will find it for you.  With conventional
    copy command, the source file path must be known.

    And this engine does not really touch the dest file but only read
    the source file. Everything else is taken care of by moban
    templating mechanism.
    """

    ACTION_IN_PRESENT_CONTINUOUS_TENSE = "Copying"
    ACTION_IN_PAST_TENSE = "Copied"

    def __init__(self, template_fs, extensions=None):
        self.template_fs = template_fs

    def get_template(self, template_file):
        return self.template_fs.readbytes(template_file)

    def get_template_from_string(self, string):
        return string

    def apply_template(self, template, *_):
        return template
