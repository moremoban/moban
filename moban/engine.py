import os

from collections import defaultdict
from jinja2 import Environment, FileSystemLoader

from moban.hashstore import HashStore
from moban.filters.text import split_length
from moban.filters.github import github_expand
import moban.utils as utils
import moban.constants as constants
import moban.exceptions as exceptions
import moban.reporter as reporter


class EngineFactory(object):
    @staticmethod
    def get_engine(template_type):
        if template_type == constants.DEFAULT_TEMPLATE_TYPE:
            return Engine
        else:
            try:
                external_engine = utils.load_external_engine(template_type)
            except ImportError:
                raise exceptions.NoThirdPartyEngine(
                    constants.MESSAGE_NO_THIRD_PARTY_ENGINE)
            return external_engine.get_engine(template_type)


class Engine(object):
    def __init__(self, template_dirs, context_dirs):
        verify_the_existence_of_directories(template_dirs)
        template_loader = FileSystemLoader(template_dirs)
        self.jj2_environment = Environment(
            loader=template_loader,
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True)
        self.jj2_environment.filters['split_length'] = split_length
        self.jj2_environment.filters['github_expand'] = github_expand
        self.context = Context(context_dirs)
        self.hash_store = HashStore()
        self.__file_count = 0
        self.__templated_count = 0

    def render_to_file(self, template_file, data_file, output_file):
        template = self.jj2_environment.get_template(template_file)
        data = self.context.get_data(data_file)
        reporter.report_templating(template_file, output_file)

        with open(output_file, 'wb') as output:
            rendered_content = template.render(**data)
            output.write(rendered_content.encode('utf-8'))

        utils.file_permissions_copy(template_file, output_file)

    def render_to_files(self, array_of_param_tuple):
        sta = Strategy(array_of_param_tuple)
        sta.process()
        choice = sta.what_to_do()
        if choice == Strategy.DATA_FIRST:
            self._render_with_finding_data_first(sta.data_file_index)
        else:
            self._render_with_finding_template_first(sta.template_file_index)
        self.hash_store.close()

    def report(self):
        if self.__templated_count == 0:
            reporter.report_no_action()
        elif self.__templated_count == self.__file_count:
            reporter.report_full_run(self.__file_count)
        else:
            reporter.report_partial_run(self.__templated_count,
                                        self.__file_count)

    def number_of_templated_files(self):
        return self.__templated_count

    def _render_with_finding_template_first(self, template_file_index):
        for (template_file, data_output_pairs) in template_file_index.items():
            template = self.jj2_environment.get_template(template_file)
            for (data_file, output) in data_output_pairs:
                data = self.context.get_data(data_file)
                flag = self._apply_template(template, data, output)
                if flag:
                    reporter.report_templating(template_file, output)
                    self.__templated_count += 1
                self.__file_count += 1

    def _render_with_finding_data_first(self, data_file_index):
        for (data_file, template_output_pairs) in data_file_index.items():
            data = self.context.get_data(data_file)
            for (template_file, output) in template_output_pairs:
                template = self.jj2_environment.get_template(template_file)
                flag = self._apply_template(template, data, output)
                if flag:
                    reporter.report_templating(template_file, output)
                    self.__templated_count += 1
                self.__file_count += 1

    def _apply_template(self, template, data, output):
        rendered_content = template.render(**data).encode('utf-8')
        flag = self.hash_store.is_file_changed(
            output, rendered_content, template.filename)
        if flag:
            with open(output, 'wb') as out:
                out.write(rendered_content)

            utils.file_permissions_copy(template.filename, output)
        return flag


class Context(object):
    def __init__(self, context_dirs):
        verify_the_existence_of_directories(context_dirs)
        self.context_dirs = context_dirs
        self.__cached_environ_variables = dict(
            (key, os.environ[key]) for key in os.environ)

    def get_data(self, file_name):
        data = utils.open_yaml(self.context_dirs, file_name)
        utils.merge(data, self.__cached_environ_variables)
        return data


class Strategy(object):
    DATA_FIRST = 1
    TEMPLATE_FIRST = 2

    def __init__(self, array_of_param_tuple):
        self.data_file_index = defaultdict(list)
        self.template_file_index = defaultdict(list)
        self.tuples = array_of_param_tuple

    def process(self):
        for (template_file, data_file, output_file) in self.tuples:
            _append_to_array_item_to_dictionary_key(
                self.data_file_index,
                data_file,
                (template_file, output_file)
            )
            _append_to_array_item_to_dictionary_key(
                self.template_file_index,
                template_file,
                (data_file, output_file)
            )

    def what_to_do(self):
        choice = Strategy.DATA_FIRST
        if self.data_file_index == {}:
            choice = Strategy.TEMPLATE_FIRST
        elif self.template_file_index != {}:
            data_files = len(self.data_file_index)
            template_files = len(self.template_file_index)
            if data_files > template_files:
                choice = Strategy.TEMPLATE_FIRST
        return choice


def _append_to_array_item_to_dictionary_key(adict, key, array_item):
    if array_item in adict[key]:
        raise exceptions.MobanfileGrammarException(
            constants.MESSAGE_SYNTAX_ERROR % (array_item, key))
    else:
        adict[key].append(array_item)


def verify_the_existence_of_directories(dirs):
    if not isinstance(dirs, list):
        dirs = [dirs]
    for directory in dirs:
        if os.path.exists(directory):
            continue
        should_I_ignore = (
            constants.DEFAULT_CONFIGURATION_DIRNAME in directory or
            constants.DEFAULT_TEMPLATE_DIRNAME in directory
        )
        if should_I_ignore:
            # ignore
            pass
        else:
            raise exceptions.DirectoryNotFound(
                constants.MESSAGE_DIR_NOT_EXIST % os.path.abspath(
                    directory))
