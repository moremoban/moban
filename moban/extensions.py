from lml.plugin import PluginManager, PluginInfo
import moban.constants as constants


class JinjaFilterManager(PluginManager):
    def __init__(self):
        super(JinjaFilterManager, self).__init__(
            constants.JINJA_FILTER_EXTENSION
            )

    def get_all_filters(self):
        for name, filter_function in self.registry.items():
            # only the first matching one is returned
            the_filter = self.load_me_now(name)
            yield (name, the_filter)


class JinjaFilter(PluginInfo):
    def __init__(self, filter_name):
        super(JinjaFilter, self).__init__(constants.JINJA_FILTER_EXTENSION,
                                          tags=[filter_name])
