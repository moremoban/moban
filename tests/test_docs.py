import os
from textwrap import dedent

from nose.tools import eq_

from . import utils


def custom_dedent(long_texts):
    refined = dedent(long_texts)
    if refined.startswith("\n"):
        refined = refined[1:]
    return refined


class TestTutorial(utils.Docs):
    def test_level_1(self):
        expected = "world"
        folder = "level-1-jinja2-cli"
        self._moban(folder, expected)

    def test_level_2(self):
        expected = """
        ========header============

        world

        ========footer============
        """
        expected = custom_dedent(expected)
        folder = "level-2-template-inheritance"
        self._moban(folder, expected)

    def test_level_3(self):
        expected = """
        ========header============

        world

        shijie

        ========footer============
        """
        expected = custom_dedent(expected)
        folder = "level-3-data-override"
        self._moban(folder, expected)

    def test_level_4(self):
        expected = """
        ========header============

        world

        shijie

        ========footer============
        """
        expected = custom_dedent(expected)
        folder = "level-4-single-command"
        self._raw_moban(["moban"], folder, expected, "a.output")

    def test_level_5(self):
        expected = """
        ========header============

        world

        shijie

        this demonstrates jinja2's include statement

        ========footer============
        """
        expected = custom_dedent(expected)
        folder = "level-5-custom-configuration"
        self._raw_moban(["moban"], folder, expected, "a.output")

    def test_level_6(self):
        expected = """
        ========header============

        world2

        shijie

        this demonstrates jinja2's include statement

        ========footer============
        """
        expected = custom_dedent(expected)
        folder = "level-6-complex-configuration"
        self._raw_moban(["moban"], folder, expected, "a.output2")

    def test_level_20(self):
        expected = """
        ========header============

        world2

        shijie

        this demonstrates jinja2's include statement

        ========footer============
        """
        expected = custom_dedent(expected)
        folder = "level-20-templates-configs-in-zip-or-tar"
        self._raw_moban_with_fs(
            ["moban"], folder, expected, "zip://a.zip!/a.output2"
        )

    def test_level_7(self):
        expected = """
        Hello, you are in level 7 example

        Hello, you are not in level 7
        """
        expected = custom_dedent(expected)

        folder = "level-7-use-custom-jinja2-filter-test-n-global"
        self._raw_moban(["moban"], folder, expected, "test.output")

    def test_level_8(self):
        expected = "it is a test\n"
        folder = "level-8-pass-a-folder-full-of-templates"
        check_file = os.path.join("templated-folder", "my")
        self._raw_moban(["moban"], folder, expected, check_file)

    def test_level_9(self):
        expected = "pypi-mobans: moban dependency as pypi package"
        folder = "level-9-moban-dependency-as-pypi-package"
        self._raw_moban(["moban"], folder, expected, "test.txt")

    def test_level_9_deprecated(self):
        expected = "pypi-mobans: moban dependency as pypi package"
        folder = "deprecated-level-9-moban-dependency-as-pypi-package"
        self._raw_moban(["moban"], folder, expected, "test.txt")

    def test_level_10(self):
        expected = "pypi-mobans: moban dependency as git repo"
        folder = "level-10-moban-dependency-as-git-repo"
        self._raw_moban(["moban"], folder, expected, "test.txt")

    def test_level_10_deprecated(self):
        expected = "pypi-mobans: moban dependency as git repo"
        folder = "deprecated-level-10-moban-dependency-as-git-repo"
        self._raw_moban(["moban"], folder, expected, "test.txt")

    def test_level_11(self):
        expected = "handlebars does not support inheritance\n"
        folder = "level-11-use-handlebars"
        self._raw_moban(["moban"], folder, expected, "a.output")

    def test_level_12(self):
        expected_a = """
        world
        world
        world
        world
        """
        expected_b = """
        142
        42
        142
        """
        expected_a = custom_dedent(expected_a)
        expected_b = custom_dedent(expected_b)
        folder = "level-12-use-template-engine-extensions"
        os.chdir(os.path.join("docs", folder))
        utils.run_moban(
            ["moban"],
            folder,
            [("a.output", expected_a), ("b.output", expected_b)],
        )

    def test_level_13_json(self):
        expected = """
        ========header============

        world from child.json

        shijie from parent.yaml

        ========footer============
        """
        expected = custom_dedent(expected)
        folder = "level-13-any-data-override-any-data"
        commands = ["moban", "-c", "child.json", "-t", "a.template"]
        self._raw_moban(commands, folder, expected, "moban.output")

    def test_level_13_yaml(self):
        expected = """
        ========header============

        world from child.yaml

        shijie from parent.json

        ========footer============
        """
        expected = custom_dedent(expected)
        folder = "level-13-any-data-override-any-data"
        commands = ["moban", "-c", "child.yaml", "-t", "a.template"]
        self._raw_moban(commands, folder, expected, "moban.output")

    def test_level_14_custom(self):
        expected = """
        ========header============

        world from child.cusom

        shijie from parent.json

        ========footer============
        """
        expected = custom_dedent(expected)
        folder = "level-14-custom-data-loader"
        commands = ["moban"]
        self._raw_moban(commands, folder, expected, "a.output")

    def test_level_15_copy_templates_as_target(self):
        expected = "test file\n"

        folder = "level-15-copy-templates-as-target"
        self._raw_moban(["moban"], folder, expected, "simple.file")

        utils.verify_content(
            "target_without_template_type",
            "file extension will trigger copy engine\n",
        )
        utils.verify_content(
            "target_in_short_form",
            (
                "it is OK to have a short form, "
                + "but the file to be 'copied' shall have 'copy' extension, "
                + "so as to trigger ContentForwardEngine, 'copy' engine.\n"
            ),
        )

    def test_level_21_copy_templates_into_zips(self):
        expected = "test file\n"

        folder = "level-21-copy-templates-into-an-alien-file-system"
        criterias = [
            ["zip://my.zip!/simple.file", expected],
            [
                "zip://my.zip!/target_without_template_type",
                "file extension will trigger copy engine\n",
            ],
            [
                "zip://my.zip!/target_in_short_form",
                (
                    "it is OK to have a short form, "
                    + "but the file to be 'copied' shall have 'copy' extension, "
                    + "so as to trigger ContentForwardEngine, 'copy' engine.\n"
                ),
            ],
        ]
        self._raw_moban_with_fs2(["moban"], folder, criterias)

    def test_level_16_group_targets_using_template_type(self):
        expected = "test file\n"

        folder = "level-16-group-targets-using-template-type"
        self._raw_moban(["moban"], folder, expected, "simple.file")

    def test_level_17_force_template_type_from_moban_file(self):
        expected = "test file\n"

        folder = "level-17-force-template-type-from-moban-file"
        self._raw_moban(["moban"], folder, expected, "simple.file")

    def test_level_18_user_defined_template_types(self):
        from datetime import datetime

        expected = "{date}\n".format(date=datetime.now().strftime("%Y-%m-%d"))

        folder = "level-18-user-defined-template-types"
        self._raw_moban(["moban"], folder, expected, "a.output")

        utils.verify_content("b.output", "shijie\n")

    def test_level_19_without_group_target(self):
        expected = "test file\n"

        folder = "level-19-moban-a-sub-group-in-targets"
        self._raw_moban(["moban"], folder, expected, "simple.file")
        utils.verify_content(
            "a.output", "I will not be selected in level 19\n"
        )
        os.unlink("a.output")

    def test_level_19_with_group_target(self):
        expected = "test file\n"

        folder = "level-19-moban-a-sub-group-in-targets"
        self._raw_moban(
            ["moban", "-g", "copy"], folder, expected, "simple.file"
        )
        # make sure only copy target is executed
        eq_(False, os.path.exists("a.output"))

    def test_misc_1(self):
        expected = "test file\n"

        folder = "misc-1-copying-templates"
        self._raw_moban(["moban"], folder, expected, "simple.file")

    def _moban(self, folder, expected):
        args = ["moban", "-c", "data.yml", "-t", "a.template"]
        self._raw_moban(args, folder, expected, "moban.output")

    def _raw_moban(self, args, folder, expected, output):
        os.chdir(os.path.join("docs", folder))
        utils.run_moban(args, folder, [(output, expected)])

    def _raw_moban_with_fs(self, args, folder, expected, output):
        os.chdir(os.path.join("docs", folder))
        utils.run_moban_with_fs(args, folder, [(output, expected)])

    def _raw_moban_with_fs2(self, args, folder, criterias):
        os.chdir(os.path.join("docs", folder))
        utils.run_moban_with_fs(args, folder, criterias)
