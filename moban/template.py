import os
import sys
import yaml
import argparse
from jinja2 import Environment, FileSystemLoader


def merge(user, default):
    if isinstance(user,dict) and isinstance(default,dict):
        for k,v in default.iteritems():
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
            raise Exception("File %s does not exist" % the_file)
    with open(the_file, 'r') as f:
        x=yaml.load(f)
        y = None
        if 'overrides' in x:
            y = open_yaml(base_dir, x.pop('overrides'))
        if y:
            return merge(x, y)
        else:
            return x


def main():
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument('-cd', '--configuration_dir',
                        default=os.path.join(".", "config"))
    parser.add_argument('-c', '--configuration')
    parser.add_argument('-td','--template_dir', nargs="*",
                        default=os.path.join(".", "templates"))
    parser.add_argument('-t', '--template')
    parser.add_argument('-o', '--output', default="a.output")
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(0)
    options = parser.parse_args()
    if options.configuration is None:
        parser.print_help()
        sys.exit(-1)
    if options.template is None:
        parser.print_help()
        sys.exit(-1)
    templateLoader = FileSystemLoader(options.template_dir)
    env = Environment(loader=templateLoader, trim_blocks=True, lstrip_blocks=True)    
    variables = open_yaml(options.configuration_dir,
                          options.configuration)
    template = env.get_template(options.template)
    with open(options.output, 'w') as f:
        f.write(template.render(**variables))


if __name__ == "__main__":
    main()