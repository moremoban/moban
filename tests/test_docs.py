import os

from nose.tools import eq_

from .utils import Docs, custom_dedent


class TestTutorial(Docs):
    def test_level_1(self):
        expected = "world"
        folder = "level-1-jinja2-cli"
        self._moban(folder, expected)

    def test_level_1_custom_define(self):
        expected = "maailman"
        folder = "level-1-jinja2-cli"
        args = [
            "moban",
            "-d",
            "hello=maailman",
            "-t",
            "a.template",
            "-o",
            "moban.output",
        ]
        self.run_moban(args, folder, [("moban.output", expected)])

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
        self.run_moban(["moban"], folder, [("a.output", expected)])

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
        self.run_moban(["moban"], folder, [("a.output", expected)])

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
        self.run_moban(["moban"], folder, [("a.output2", expected)])

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
        self.run_moban_with_fs(
            ["moban"], folder, [("zip://a.zip!/a.output2", expected)]
        )

    def test_level_7(self):
        expected = """
        Hello, you are in level 7 example

        Hello, you are not in level 7
        """
        expected = custom_dedent(expected)

        folder = "level-7-use-custom-jinja2-filter-test-n-global"
        self.run_moban(["moban"], folder, [("test.output", expected)])

    def test_level_8(self):
        expected = "it is a test\n"
        folder = "level-8-pass-a-folder-full-of-templates"
        check_file = os.path.join("templated-folder", "my")
        self.run_moban(["moban"], folder, [(check_file, expected)])

    def test_level_9(self):
        expected = "pypi-mobans: moban dependency as pypi package"
        folder = "level-9-moban-dependency-as-pypi-package"
        self.run_moban(["moban"], folder, [("test.txt", expected)])

    def test_level_24(self):
        expected = "pypi-mobans: files over http protocol"
        folder = "level-24-files-over-http"
        self.run_moban(["moban"], folder, [("test.txt", expected)])

    def test_level_9_deprecated(self):
        expected = "pypi-mobans: moban dependency as pypi package"
        folder = "deprecated-level-9-moban-dependency-as-pypi-package"
        self.run_moban(["moban"], folder, [("test.txt", expected)])

    def test_level_10(self):
        expected = "pypi-mobans: moban dependency as git repo"
        folder = "level-10-moban-dependency-as-git-repo"
        self.run_moban(["moban"], folder, [("test.txt", expected)])

    def test_level_10_deprecated(self):
        expected = "pypi-mobans: moban dependency as git repo"
        folder = "deprecated-level-10-moban-dependency-as-git-repo"
        self.run_moban(["moban"], folder, [("test.txt", expected)])

    def test_level_11(self):
        expected = "handlebars does not support inheritance\n"
        folder = "level-11-use-handlebars"
        self.run_moban(["moban"], folder, [("a.output", expected)])

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
        self.run_moban(
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
        commands = [
            "moban",
            "-c",
            "child.json",
            "-t",
            "a.template",
            "-o",
            "moban.output",
        ]
        self.run_moban(commands, folder, [("moban.output", expected)])

    def test_level_13_yaml(self):
        expected = """
        ========header============

        world from child.yaml

        shijie from parent.json

        ========footer============
        """
        expected = custom_dedent(expected)
        folder = "level-13-any-data-override-any-data"
        commands = [
            "moban",
            "-c",
            "child.yaml",
            "-t",
            "a.template",
            "-o",
            "moban.output",
        ]
        self.run_moban(commands, folder, [("moban.output", expected)])

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
        self.run_moban(commands, folder, [("a.output", expected)])

    def test_level_15_copy_templates_as_target(self):
        expected = "test file\n"

        folder = "level-15-copy-templates-as-target"
        assertions = [
            ("simple.file", expected),
            (
                "target_without_template_type",
                "file extension will trigger copy engine\n",
            ),
            (
                "target_in_short_form",
                (
                    "it is OK to have a short form, "
                    + "but the file to be 'copied' shall have 'copy' extension, "
                    + "so as to trigger ContentForwardEngine, 'copy' engine.\n"
                ),
            ),
            (
                "output_is_copied.same_file_extension",
                "it is implicit copy as well",
            ),
        ]
        self.run_moban(["moban"], folder, assertions)

    def test_level_21_copy_templates_into_zips(self):
        expected = "test file\n"

        folder = "level-21-copy-templates-into-an-alien-file-system"
        long_url = (
            "zip://my.zip!/test-recursive-dir/sub_directory_is_copied"
            + "/because_star_star_is_specified.txt"
        )
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
            ["zip://my.zip!/test-dir/afile.txt", "dir for copying\n"],
            [long_url, "dest_directory: source_directory/**\n"],
        ]
        self.run_moban_with_fs(["moban"], folder, criterias)

    def test_level_16_group_targets_using_template_type(self):
        expected = "test file\n"

        folder = "level-16-group-targets-using-template-type"
        self.run_moban(["moban"], folder, [("simple.file", expected)])

    def test_level_17_force_template_type_from_moban_file(self):
        expected = "test file\n"

        folder = "level-17-force-template-type-from-moban-file"
        self.run_moban(["moban"], folder, [("simple.file", expected)])

    def test_level_18_user_defined_template_types(self):
        from datetime import datetime

        expected = "{date}\n".format(date=datetime.now().strftime("%Y-%m-%d"))

        folder = "level-18-user-defined-template-types"
        self.run_moban(
            ["moban"],
            folder,
            [("a.output", expected), ("b.output", "shijie\n")],
        )

    def test_level_19_without_group_target(self):
        expected = "test file\n"

        folder = "level-19-moban-a-sub-group-in-targets"
        assertions = [
            ("simple.file", expected),
            ("a.output", "I will not be selected in level 19\n"),
        ]
        self.run_moban(["moban"], folder, assertions)

    def test_level_19_with_group_target(self):
        expected = "test file\n"

        folder = "level-19-moban-a-sub-group-in-targets"
        self.run_moban(
            ["moban", "-g", "copy"], folder, [("simple.file", expected)]
        )
        # make sure only copy target is executed
        eq_(False, os.path.exists("a.output"))

    def test_level_22_intermediate_targets(self):
        expected = "a world\n"

        folder = "level-22-intermediate-targets"
        self.run_moban(["moban"], folder, [("final", expected)])
        assert os.path.exists("intermediate.jj2")

    def test_level_25_delete_intermediate_targets(self):
        expected = "a world\n"

        folder = "level-25-delete-intermediate-targets"
        self.run_moban(["moban"], folder, [("final", expected)])
        assert not os.path.exists("intermediate.jj2")
        assert not os.path.exists("intermediate2.jj2")
        assert not os.path.exists("intermediate3.jj2")

    def test_level_26_strip_intermediate_targets(self):
        expected = "a world"

        folder = "level-26-strip-rendered-content"
        self.run_moban(["moban"], folder, [("final", expected)])
        assert not os.path.exists("intermediate.strip")

    def test_level_23_inherit_parent_moban_file(self):
        folder = "level-23-inherit-organisational-moban-file"
        self.run_moban(
            ["moban"],
            folder,
            [("output_a", "I am template a"), ("output_b", "I am template b")],
        )

    def test_misc_1(self):
        expected = "test file\n"

        folder = "misc-1-copying-templates"
        self.run_moban(["moban"], folder, [("simple.file", expected)])

    def _moban(self, folder, expected):
        args = [
            "moban",
            "-c",
            "data.yml",
            "-t",
            "a.template",
            "-o",
            "moban.output",
        ]
        self.run_moban(args, folder, [("moban.output", expected)])
