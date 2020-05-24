import logging

from lml.plugin import PluginInfo

from moban import constants

LOG = logging.getLogger(__name__)


class ContentProcessor(PluginInfo):
    """
    @ContentProcessor('strip', 'Stripping', 'Stripped'):
    def strip(template_file: str) -> str:
        ret = template_file.strip()
        return ret
    """

    def __init__(self, action, action_continuing_tense, action_past_tense):
        super(ContentProcessor, self).__init__(
            constants.TEMPLATE_ENGINE_EXTENSION, tags=[action]
        )
        self.action = action
        self.action_continuing_tense = action_continuing_tense
        self.action_past_tense = action_continuing_tense

    def __call__(self, a_content_processor_function):
        continuing_tense = self.action_continuing_tense
        past_tense = self.action_past_tense

        class CustomEngine(object):
            ACTION_IN_PRESENT_CONTINUOUS_TENSE = continuing_tense
            ACTION_IN_PAST_TENSE = past_tense

            def __init__(self, template_fs, extensions=None):
                self.template_fs = template_fs

            def get_template(self, template_file):
                content = self.template_fs.readbytes(template_file)
                ret = a_content_processor_function(content)
                return ret

            def get_template_from_string(self, a_string):
                ret = a_content_processor_function(a_string)
                return ret

            def apply_template(self, template, *_):
                ret = a_content_processor_function(template)
                return ret

        super(ContentProcessor, self).__call__(CustomEngine)
        return a_content_processor_function
