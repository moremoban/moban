import fs.path
from mock import patch
from nose.tools import eq_
from moban.definitions import TemplateTarget


class TestFinder:
    def setUp(self):
        self.patcher = patch("moban.file_system.exists")
        self.fake_file_existence = self.patcher.start()
        self.fake_file_existence.__name__ = "fake"
        self.fake_file_existence.__module__ = "fake"

    def tearDown(self):
        self.patcher.stop()

    def test_moban_yml(self):
        self.fake_file_existence.return_value = True
        from moban.mobanfile import find_default_moban_file

        actual = find_default_moban_file()
        eq_(".moban.yml", actual)

    def test_moban_yaml(self):
        self.fake_file_existence.side_effect = [False, True]
        from moban.mobanfile import find_default_moban_file

        actual = find_default_moban_file()
        eq_(".moban.yaml", actual)

    def test_no_moban_file(self):
        self.fake_file_existence.side_effect = [False, False]
        from moban.mobanfile import find_default_moban_file

        actual = find_default_moban_file()
        assert actual is None


@patch("moban.core.moban_factory.MobanEngine.render_to_files")
def test_handle_targets(fake_renderer):
    from moban.mobanfile import handle_targets

    TEMPLATE = "copier-test01.csv"
    OUTPUT = "output.csv"
    CONFIGURATION = "child.yaml"
    TEMPLATE_DIRS = [fs.path.join("tests", "fixtures")]
    DEFAULT_TEMPLATE_TYPE = "jinja2"

    options = dict(
        configuration=CONFIGURATION,
        template_type=DEFAULT_TEMPLATE_TYPE,
        template_dir=TEMPLATE_DIRS,
        configuration_dir=fs.path.join("tests", "fixtures"),
    )
    short_hand_targets = [{OUTPUT: TEMPLATE}]
    handle_targets(options, short_hand_targets)

    call_args = list(fake_renderer.call_args[0][0])
    eq_(
        call_args,
        [
            TemplateTarget(
                "copier-test01.csv",
                "child.yaml",
                "output.csv",
                template_type="jinja2",
            )
        ],
    )


@patch("moban.core.moban_factory.MobanEngine.render_to_files")
def test_handle_targets_sequence(fake_renderer):
    from moban.mobanfile import handle_targets

    TEMPLATE1 = "a.template.jj2"
    OUTPUT1 = "filterme.handlebars"  # in the future, this could dynamic output
    OUTPUT2 = "filtered_output.txt"
    CONFIGURATION = "child.yaml"
    TEMPLATE_DIRS = [fs.path.join("tests", "fixtures", "mobanfile")]
    DEFAULT_TEMPLATE_TYPE = "jinja2"

    options = dict(
        configuration=CONFIGURATION,
        template_type=DEFAULT_TEMPLATE_TYPE,
        template_dir=TEMPLATE_DIRS,
        configuration_dir=fs.path.join("tests", "fixtures"),
    )
    short_hand_targets = [{OUTPUT1: TEMPLATE1}, {OUTPUT2: OUTPUT1}]
    handle_targets(options, short_hand_targets)

    call_args = list(fake_renderer.call_args_list)

    eq_(
        call_args[0][0][0][0],
        TemplateTarget(
            "a.template.jj2",
            "child.yaml",
            "filterme.handlebars",
            template_type="jj2",
        ),
    )
    eq_(
        call_args[1][0][0][0],
        TemplateTarget(
            "filterme.handlebars",
            "child.yaml",
            "filtered_output.txt",
            template_type="handlebars",
        ),
    )
