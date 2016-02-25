"""
    moban.template
    ~~~~~~~~~~~~~~~~~~~

    Bring jinja2 to command line

    :copyright: (c) 2016 by Onni Software Ltd.
    :license: MIT License, see LICENSE for more details

"""

import os
import sys
import argparse

import yaml
from jinja2 import Environment, FileSystemLoader

# Configurations
PROGRAM_NAME = 'moban'
PROGRAM_DESCRIPTION = 'Yet another jinja2 cli command for static text generation'
DEFAULT_YAML_SUFFIX = '.yml'
# .moban.yml, default moban configuration file
DEFAULT_MOBAN_FILE = '.%s%s' % (PROGRAM_NAME, DEFAULT_YAML_SUFFIX)

# Command line options
LABEL_CONFIG = 'configuration'
LABEL_CONFIG_DIR = '%s_dir' % LABEL_CONFIG
LABEL_TEMPLATE = 'template'
LABEL_TMPL_DIRS = '%s_dir' % LABEL_TEMPLATE
LABEL_OVERRIDES = 'overrides'
LABEL_OUTPUT = 'output'
LABEL_TARGETS = 'targets'
DEFAULT_OPTIONS = {
    # .moban.cd, default configuration dir
    LABEL_CONFIG_DIR: os.path.join('.', '.%s.cd' % PROGRAM_NAME),
    # .moban.td, default template dirs
    LABEL_TMPL_DIRS: ['.', os.path.join('.', '.%s.td' % PROGRAM_NAME)],
    # moban.output, default output file name
    LABEL_OUTPUT: '%s.output' % PROGRAM_NAME,
    # data.yml, default data input file
    LABEL_CONFIG: 'data%s' % DEFAULT_YAML_SUFFIX
}

# I/O messages
# Message
MESSAGE_TEMPLATING = "Templating %s to %s"
# Error handling
ERROR_INVALID_MOBAN_FILE = "%s is an invalid yaml file."
ERROR_NO_TARGETS = "No targets in %s"
ERROR_NO_TEMPLATE = "No template found"
ERROR_DATA_FILE_NOT_FOUND = "Both %s and %s does not exist"
ERROR_DATA_FILE_ABSENT = "File %s does not exist"


def open_yaml(base_dir, file_name):
    """
    chained yaml loader
    """
    the_file = file_name
    if not os.path.exists(the_file):
        if base_dir:
            the_file = os.path.join(base_dir, file_name)
            if not os.path.exists(the_file):
                raise IOError(
                    ERROR_DATA_FILE_NOT_FOUND % (file_name,
                                                 the_file))
        else:
            raise IOError(ERROR_DATA_FILE_ABSENT % the_file)
    with open(the_file, 'r') as data_yaml:
        data = yaml.load(data_yaml)
        if data is not None:
            parent_data = None
            if LABEL_OVERRIDES in data:
                parent_data = open_yaml(
                    base_dir,
                    data.pop(LABEL_OVERRIDES))
            if parent_data:
                return merge(data, parent_data)
            else:
                return data
        else:
            return None


class Context(object):
    def __init__(self, context_dirs):
        self.context_dirs = context_dirs

    def get_data(self, file_name):
        return open_yaml(self.context_dirs, file_name)


class Engine(object):
    def __init__(self, template_dirs, context_dirs): 
        template_loader = FileSystemLoader(template_dirs)
        self.jj2_environment = Environment(
            loader=template_loader,
            trim_blocks=True,
            lstrip_blocks=True)
        self.context = Context(context_dirs)

    def render_to_file(self, template, data_file, output_file):
        template = self.jj2_environment.get_template(template)
        data = self.context.get_data(data_file)
        apply_template(template, data, output_file)

    def render_to_files(self, array_of_param_tuple):
        data_file_index = {}
        template_file_index = {}
        data_set = set()
        template_set = set()
        for (template_file, data_file, output_file) in array_of_param_tuple:
            data_set.add(data_file)
            template_set.add(template_file)
            if data_file not in data_file_index:
                data_file_index[data_file] = []
            if template_file not in template_file_index:
                template_file_index[template_file] = []
            data_file_index[data_file].append((template_file, output_file))
            template_file_index[template_file].append((data_file, output_file))
        if len(template_set) == 0:
            self._render_with_finding_data_first(data_file_index)
        elif len(data_set) == 0:
            self._render_with_finding_template_first(template_file_index)
        elif len(template_set) < len(data_set):
            self._render_with_finding_template_first(template_file_index)
        else:
            self._render_with_finding_data_first(data_file_index)

    def _render_with_finding_template_first(self, template_file_index):
        for (template_file, data_output_pairs) in template_file_index.items():
            template = self.jj2_environment.get_template(template_file)
            for (data_file, output) in data_output_pairs:
                print(MESSAGE_TEMPLATING % (template_file, output))
                data = self.context.get_data(data_file)
                apply_template(template, data, output)

    def _render_with_finding_data_first(self, data_file_index):
        for (data_file, template_output_pairs) in data_file_index.items():
            data = self.context.get_data(data_file)
            for (template_file, output) in template_output_pairs:
                print(MESSAGE_TEMPLATING % (template_file, output))
                template = self.jj2_environment.get_template(template_file)
                apply_template(template, data, output)

        
def main():
    """
    program entry point
    """
    parser = create_parser()
    if os.path.exists(DEFAULT_MOBAN_FILE):
        handle_moban_file(parser)
    else:
        handle_command_line(parser)


def create_parser():
    """
    construct the program options
    """
    parser = argparse.ArgumentParser(
        prog=PROGRAM_NAME,
        description=PROGRAM_DESCRIPTION)
    parser.add_argument(
        '-cd', '--%s' % LABEL_CONFIG_DIR,
        help="the directory for configuration file lookup"
    )
    parser.add_argument(
        '-c', '--%s' % LABEL_CONFIG,
        help="the dictionary file"
    )
    parser.add_argument(
        '-td', '--%s' % LABEL_TMPL_DIRS, nargs="*",
        help="the directories for template file lookup"
    )
    parser.add_argument(
        '-t', '--%s' % LABEL_TEMPLATE,
        help="the template file"
    )
    parser.add_argument(
        '-o', '--%s' % LABEL_OUTPUT,
        help="the output file"
    )
    return parser


def handle_moban_file(parser):
    """
    act upon default moban file
    """
    options = {}
    if len(sys.argv) > 1:
        options = vars(parser.parse_args())
    more_options = open_yaml(None, DEFAULT_MOBAN_FILE)
    if more_options is None:
        print(ERROR_INVALID_MOBAN_FILE % DEFAULT_MOBAN_FILE)
        sys.exit(-1)
    if LABEL_TARGETS not in more_options:
        print(ERROR_NO_TARGETS % DEFAULT_MOBAN_FILE)
        sys.exit(0)
    if LABEL_CONFIG in more_options:
        options = merge(options, more_options[LABEL_CONFIG])
    options = merge(options, DEFAULT_OPTIONS)
    list_of_templating_parameters = translate_targets(
        options,
        more_options[LABEL_TARGETS])    
    engine = Engine(options[LABEL_TMPL_DIRS], options[LABEL_CONFIG_DIR])
    engine.render_to_files(list_of_templating_parameters)


def handle_command_line(parser):
    """
    act upon command options
    """
    options = vars(parser.parse_args())
    options = merge(options, DEFAULT_OPTIONS)
    if options[LABEL_TEMPLATE] is None:
        print(ERROR_NO_TEMPLATE)
        parser.print_help()
        sys.exit(-1)
    engine = Engine(options[LABEL_TMPL_DIRS], options[LABEL_CONFIG_DIR])
    engine.render_to_file(
        options[LABEL_TEMPLATE],
        options[LABEL_CONFIG],
        options[LABEL_OUTPUT]
    )


def merge(left, right):
    """
    deep merge dictionary on the left with the one
    on the right.

    Fill in left dictionary with right one where
    the value of the key from the right one in
    the left one is missing or None.
    """
    if isinstance(left, dict) and isinstance(right, dict):
        for key, value in right.items():
            if key not in left:
                left[key] = value
            elif left[key] is None:
                left[key] = value
            else:
                left[key] = merge(left[key], value)
    return left


def translate_targets(options, targets):
    common_data_file = options[LABEL_CONFIG]
    for target in targets:
        if LABEL_OUTPUT in target:
            template_file = target.get(LABEL_TEMPLATE, options.get(LABEL_TEMPLATE, None))
            data_file = target.get(LABEL_CONFIG, common_data_file)
            output = target[LABEL_OUTPUT]
            yield((template_file, data_file, output))
        else:
            for output, template_file in target.items():
                yield((template_file, common_data_file, output))


def apply_template(jj2_template, data, output_file):
    """
    write templated result
    """
    with open(output_file, 'w') as output:
        content = jj2_template.render(**data)
        output.write(content)