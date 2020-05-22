import fs
from lml.plugin import PluginInfo

from moban import constants
from moban.core.mobanfile.store import STORE


@PluginInfo(
    constants.TEMPLATE_ENGINE_EXTENSION, tags=[constants.TEMPLATE_DELETE]
)
class DeleteEngine(object):
    """
    Does no templating but delete generated intermediate targets

    """

    ACTION_IN_PRESENT_CONTINUOUS_TENSE = "Deleting"
    ACTION_IN_PAST_TENSE = "Deleted"

    def __init__(self, template_fs, extensions=None):
        self.template_fs = template_fs

    def get_template(self, template_file):
        if template_file in STORE.intermediate_targets:
            with fs.open_fs(".") as the_fs:
                if the_fs.exists(template_file):
                    the_fs.remove(template_file)
                    return True
                else:
                    return False
        else:
            raise Exception(f"Cannot remove {template_file}")

    def get_template_from_string(self, string):
        raise NotImplementedError("Not sure what to do")

    def apply_template(self, template, *_):
        raise NotImplementedError("Not sure what to do")
