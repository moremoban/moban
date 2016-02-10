"""
    moban.template
    ~~~~~~~~~~~~~~~~~~~

    Bring jinja2 to command line

    :copyright: (c) 2016 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details

"""

import os
import sys
import argparse

import yaml
from jinja2 import Environment, FileSystemLoader


PY2 = sys.version_info[0] == 2
DEFAULT_MOBAN_FILE = '.moban.yaml'
DEFAULT_OPTIONS = {
    'configuration': 'data.yaml',
    'configuration_dir': os.path.join('.', 'config'),
    'template_dir': ['.', os.path.join('.', 'templates')]
}


def main():
    """
    program entry point
    """
    parser = create_parser()
    options = vars(parser.parse_args())
    if os.path.exists(DEFAULT_MOBAN_FILE):
        more_options = open_yaml(None, DEFAULT_MOBAN_FILE)
        if more_options is None:
            print("%s is an invalid yaml file." % DEFAULT_MOBAN_FILE)
            parser.print_help()
            sys.exit(-1)
        if 'targets' not in more_options:
            print("No targets in %s" % DEFAULT_MOBAN_FILE)
            sys.exit(0)
        tmp_dict = {}
        if 'configuration' in more_options:
            for config in more_options['configuration']:
                for key, value in config.items():
                    tmp_dict[key] = value
        options = merge(options, tmp_dict)
        options = merge(options, DEFAULT_OPTIONS)
        data = open_yaml(options['configuration_dir'],
                         options['configuration'])
        for target in more_options['targets']:
            for key, value in target.items():
                options['template'] = value
                options['output'] = key
                do_template(options, data)
    else:
        options = merge(options, DEFAULT_OPTIONS)
        if options['template'] is None:
            parser.print_help()
            sys.exit(-1)
        data = open_yaml(options['configuration_dir'],
                         options['configuration'])
        do_template(options, data)


def merge(left, right):
    """
    deep merge dictionary on the left with the one
    on the right.

    Fill in left dictionary with right one where
    the value of the key from the right one in
    the left one is missing or None.
    """
    if isinstance(left, dict) and isinstance(right, dict):
        for key, value in _get_dict_items(right):
            if key not in left:
                left[key] = value
            elif left[key] is None:
                left[key] = value
            else:
                left[key] = merge(left[key], value)
    return left


def open_yaml(base_dir, file_name):
    """
    chained yaml loader
    """
    the_file = file_name
    if not os.path.exists(the_file):
        if base_dir:
            the_file = os.path.join(base_dir, file_name)
            if not os.path.exists(the_file):
                raise IOError("File %s does not exist" % the_file)
        else:
            raise IOError("File %s does not exist" % the_file)
    with open(the_file, 'r') as data_yaml:
        data = yaml.load(data_yaml)
        if data is not None:
            parent_data = None
            if 'overrides' in data:
                parent_data = open_yaml(base_dir,
                                        data.pop('overrides'))
            if parent_data:
                return merge(data, parent_data)
            else:
                return data
        else:
            return None


def do_template(options, data):
    """
    apply jinja2 here
    """
    print("Templating %s to %s" % (options['template'], options['output']))
    template_loader = FileSystemLoader(options['template_dir'])
    env = Environment(loader=template_loader,
                      trim_blocks=True,
                      lstrip_blocks=True)
    template = env.get_template(options['template'])
    with open(options['output'], 'w') as output:
        output.write(template.render(**data))


def create_parser():
    """
    construct the program options
    """
    parser = argparse.ArgumentParser(
        prog='moban',
        description="Yet another jinja2 cli command for static text generation")
    parser.add_argument(
        '-cd', '--configuration_dir',
        help="the directory for configuration file lookup"
    )
    parser.add_argument(
        '-c', '--configuration',
        help="the dictionary file"
    )
    parser.add_argument(
        '-td', '--template_dir', nargs="*",
        help="the directories for template file lookup"
    )
    parser.add_argument(
        '-t', '--template',
        help="the template file"
    )
    parser.add_argument(
        '-o', '--output',
        default="a.output",
        help="the output file"
    )
    return parser


def _get_dict_items(adict):
    if PY2:
        return adict.iteritems()
    else:
        return adict.items()
