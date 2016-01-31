import os
import sys
import yaml
import argparse
from jinja2 import Environment, FileSystemLoader

PY2 = sys.version_info[0] == 2


def get_dict_items(adict):
    if PY2:
        return adict.iteritems()
    else:
        return adict.items()


def merge(user, default):
    if isinstance(user,dict) and isinstance(default,dict):
        for k,v in get_dict_items(default):
            if k not in user:
                user[k] = v
            else:
                user[k] = merge(user[k],v)
    return user


def open_yaml(base_dir, file_name):
    the_file = file_name
    if not os.path.exists(the_file):
        the_file = os.path.join(base_dir, file_name)
        if not os.path.exists(the_file):
            raise IOError("File %s does not exist" % the_file)
    with open(the_file, 'r') as f:
        x=yaml.load(f)
        y = None
        if 'overrides' in x:
            y = open_yaml(base_dir, x.pop('overrides'))
        if y:
            return merge(x, y)
        else:
            return x


def do_template(options):
    templateLoader = FileSystemLoader(options.template_dir)
    env = Environment(loader=templateLoader,
                      trim_blocks=True,
                      lstrip_blocks=True)    
    variables = open_yaml(options.configuration_dir,
                          options.configuration)
    template = env.get_template(options.template)
    with open(options.output, 'w') as f:
        f.write(template.render(**variables))


def main():
    parser = argparse.ArgumentParser(
        description="Yet another jinja2 cli command for static text generation")
    parser.add_argument(
        '-cd', '--configuration_dir',
        default=os.path.join(".", "config"),
        help="the directory for configuration file lookup"
    )
    parser.add_argument(
        '-c', '--configuration',
        default=".moban.yaml",
        help="the dictionary file"
    )
    parser.add_argument(
        '-td','--template_dir', nargs="*",
        default=[".", os.path.join(".", "templates")],
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
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)
    options = parser.parse_args()
    if options.template is None:
        parser.print_help()
        sys.exit(-1)
    do_template(options)


if __name__ == "__main__":
    main()