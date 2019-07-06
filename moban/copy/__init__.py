from moban import utils, constants
from lml.plugin import PluginInfo


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

    def __init__(self, template_dirs, extensions=None):
        self.template_dirs = template_dirs

    def get_template(self, template_file):
        real_file_name = utils.find_file_in_template_dirs(
            template_file, self.template_dirs
        )
        with open(real_file_name, "rb") as file_handle:
            return file_handle.read()

    def get_template_from_string(self, string):
        return string

    def apply_template(self, template, *_):
        return template
