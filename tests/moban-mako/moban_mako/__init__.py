from lml.plugin import PluginInfo

from moban.constants import TEMPLATE_ENGINE_EXTENSION


@PluginInfo(TEMPLATE_ENGINE_EXTENSION, tags=["mako"])
class MakoEngine:
    def __init__(self, template_dirs):
        pass
