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
    def __init__(self):
        super(JinjaFilter, self).__init__(constants.JINJA_FILTER_EXTENSION)

    def tags(self):
        yield self.cls.__name__


class JinjaTestManager(PluginManager, PluginMixin):
    def __init__(self):
        super(JinjaTestManager, self).__init__(constants.JINJA_TEST_EXTENSION)


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


class JinjaGlobalsManager(PluginManager, PluginMixin):
    def __init__(self):
        super(JinjaGlobalsManager, self).__init__(
            constants.JINJA_GLOBALS_EXTENSION
        )


def jinja_global(identifier, dict_obj):
    plugin = PluginInfo(constants.JINJA_GLOBALS_EXTENSION, tags=[identifier])
    plugin(dict_obj)


class LibraryManager(PluginManager):
    def __init__(self):
        super(LibraryManager, self).__init__(
            constants.LIBRARY_EXTENSION
        )

    def resource_path_of(self, library_name):
        print(self.registry)
        library = self.get_a_plugin(library_name)
        return library.resources_path
