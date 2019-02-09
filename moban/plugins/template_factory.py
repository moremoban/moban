from lml.plugin import PluginManager

from moban import constants, exceptions
from moban.plugins.template_engine import TemplateEngine


class TemplateFactory(PluginManager):
    def __init__(self):
        super(TemplateFactory, self).__init__(
            constants.TEMPLATE_ENGINE_EXTENSION
        )
        self.extensions = {}

    def register_extensions(self, extensions):
        self.extensions.update(extensions)

    def get_engine(self, template_type, template_dirs, context_dirs):
        engine_cls = self.load_me_now(template_type)
        engine_extensions = self.extensions.get(template_type)
        return TemplateEngine(
            template_dirs, context_dirs, engine_cls, engine_extensions
        )

    def all_types(self):
        return list(self.registry.keys())

    def raise_exception(self, key):
        raise exceptions.NoThirdPartyEngine(key)
