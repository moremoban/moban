from moban import constants
from lml.plugin import PluginInfo


class JinjaFilter(PluginInfo):
    def __init__(self):
        super(JinjaFilter, self).__init__(constants.JINJA_FILTER_EXTENSION)

    def tags(self):
        yield self.cls.__name__


class JinjaTest(PluginInfo):
    def __init__(self, test_name=None):
        super(JinjaTest, self).__init__(constants.JINJA_TEST_EXTENSION)
        self.test_name = test_name

    def tags(self):
        if self.test_name:
            yield self.test_name
        else:
            yield self.cls.__name__


def jinja_tests(**keywords):
    for key, value in keywords.items():
        JinjaTest(key)(value)


def jinja_global(identifier, dict_obj):
    plugin = PluginInfo(constants.JINJA_GLOBALS_EXTENSION, tags=[identifier])
    plugin(dict_obj)
