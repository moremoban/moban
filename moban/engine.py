from jinja2 import Environment, FileSystemLoader

from moban.context import Context


MESSAGE_TEMPLATING = "Templating %s to %s"


class Engine(object):
    def __init__(self, template_dirs, context_dirs):
        template_loader = FileSystemLoader(template_dirs)
        self.jj2_environment = Environment(
            loader=template_loader,
            trim_blocks=True,
            lstrip_blocks=True)
        self.context = Context(context_dirs)

    def render_to_file(self, template_file, data_file, output_file):
        template = self.jj2_environment.get_template(template_file)
        data = self.context.get_data(data_file)
        print(MESSAGE_TEMPLATING % (template_file, output_file))
        apply_template(template, data, output_file)

    def render_to_files(self, array_of_param_tuple):
        sta = Strategy(array_of_param_tuple)
        sta.process()
        algo = sta.what_to_do()
        if algo == Strategy.DATA_FIRST:
            self._render_with_finding_data_first(sta.data_file_index)
        else:
            self._render_with_finding_template_first(sta.template_file_index)

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


class Strategy(object):
    DATA_FIRST = 1
    TEMPLATE_FIRST = 2

    def __init__(self, array_of_param_tuple):
        self.data_file_index = {}
        self.template_file_index = {}
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
        algo = Strategy.DATA_FIRST
        if self.data_file_index == {}:
            algo = Strategy.TEMPLATE_FIRST
        elif self.template_file_index != {}:
            data_files = len(self.data_file_index)
            template_files = len(self.template_file_index)
            if data_files > template_files:
                algo = Strategy.TEMPLATE_FIRST
        return algo


def _append_to_array_item_to_dictionary_key(adict, key, array_item):
    if key not in adict:
        adict[key] = []
    adict[key].append(array_item)
