from jinja2 import Environment, FileSystemLoader

from moban.context import Context


# Message
MESSAGE_TEMPLATING = "Templating %s to %s"


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

        
def apply_template(jj2_template, data, output_file):
    """
    write templated result
    """
    with open(output_file, 'w') as output:
        content = jj2_template.render(**data)
        output.write(content)