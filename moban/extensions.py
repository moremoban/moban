from lml.plugin import PluginManager, PluginInfo
import moban.constants as constants


class PluginMixin:

    def get_all(self):
        for name in self.registry.keys():
            # only the first matching one is returned
            the_filter = self.load_me_now(name)
            yield (name, the_filter)


class JinjaFilterManager(PluginManager, PluginMixin):
    def __init__(self):
        super(JinjaFilterManager, self).__init__(
            constants.JINJA_FILTER_EXTENSION
            )


class JinjaFilter(PluginInfo):
    def __init__(self, filter_name):
        super(JinjaFilter, self).__init__(constants.JINJA_FILTER_EXTENSION,
                                          tags=[filter_name])


class JinjaTestManager(PluginManager, PluginMixin):
    def __init__(self):
        super(JinjaTestManager, self).__init__(
            constants.JINJA_TEST_EXTENSION
            )


class JinjaTest(PluginInfo):
    def __init__(self, test_name):
        super(JinjaTest, self).__init__(
            constants.JINJA_TEST_EXTENSION,
            tags=[test_name])


def jinja_tests(**keywords):
    for key, value in keywords.items():
        JinjaTest(key)(value)


class JinjaGlobalsManager(PluginManager, PluginMixin):
    def __init__(self):
        super(JinjaGlobalsManager, self).__init__(
            constants.JINJA_GLOBALS_EXTENSION
            )


class PluginHelper(object):
    def __init__(self, identifier, payload_obj):
        self.payload = payload_obj
        self.__name__ = identifier


def jinja_global(identifier, dict_obj):
    plugin = PluginInfo(constants.JINJA_GLOBALS_EXTENSION,
                        tags=[identifier])
    helper = PluginHelper(identifier, dict_obj)
    plugin(helper)
