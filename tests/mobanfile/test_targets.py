import os
import uuid

from nose.tools import eq_, raises
from moban.mobanfile import targets
from moban.exceptions import GroupTargetNotFound
from moban.definitions import TemplateTarget

TEMPLATE = "a.jj2"
OUTPUT = "a.output"
CONFIGURATION = "data.config"
TEMPLATE_DIRS = [os.path.join("tests", "fixtures")]
DEFAULT_TEMPLATE_TYPE = "default-template-type"


def test_handling_group_target():
    group_template_type = "group-template-type"
    options = dict(
        configuration=CONFIGURATION,
        template_type=DEFAULT_TEMPLATE_TYPE,
        template_dir=TEMPLATE_DIRS,
    )
    short_hand_targets = [{OUTPUT: TEMPLATE}]

    actual = list(
        targets._handle_group_target(
            options, short_hand_targets, group_template_type
        )
    )
    expected = [
        TemplateTarget(TEMPLATE, CONFIGURATION, OUTPUT, group_template_type)
    ]
    eq_(expected, actual)


def test_extract_group_targets():
    test_targets = [
        {"output": "a.output", "template": "a.template.jj2"},
        {"copy": [{"output": "source"}], "copy1": [{"output1": "source1"}]},
    ]
    actual = targets.extract_group_targets("copy1", test_targets)
    expected = [{"copy1": [{"output1": "source1"}]}]
    eq_(expected, actual)


@raises(GroupTargetNotFound)
def test_extract_group_targets_not_found():
    test_targets = [
        {"copy": [{"output": "source"}], "copy1": [{"output1": "source1"}]}
    ]
    actual = targets.extract_group_targets("copy2", test_targets)
    expected = []
    eq_(expected, actual)


class TestImplicitTarget:
    def test_derive_template_type_from_target_template_file(self):

        options = dict(
            configuration=CONFIGURATION,
            template_type=DEFAULT_TEMPLATE_TYPE,
            template_dir=TEMPLATE_DIRS,
        )

        actual = list(
            targets._handle_implicit_target(options, TEMPLATE, OUTPUT)
        )
        expected = [TemplateTarget(TEMPLATE, CONFIGURATION, OUTPUT, "jj2")]
        eq_(expected, actual)

    def test_use_moban_default_template_from_options(self):
        template_without_suffix = "template"

        options = dict(
            configuration=CONFIGURATION,
            template_type=DEFAULT_TEMPLATE_TYPE,
            template_dir=TEMPLATE_DIRS,
        )

        actual = list(
            targets._handle_implicit_target(
                options, template_without_suffix, OUTPUT
            )
        )
        expected = [
            TemplateTarget(
                template_without_suffix,
                CONFIGURATION,
                OUTPUT,
                DEFAULT_TEMPLATE_TYPE,
            )
        ]
        eq_(expected, actual)


class TestExplicitTarget:
    def test_use_target_template_type(self):

        target = dict(template_type="use-me", template=TEMPLATE, output=OUTPUT)
        options = dict(
            configuration=CONFIGURATION,
            template_type=DEFAULT_TEMPLATE_TYPE,
            template_dir=TEMPLATE_DIRS,
        )

        actual = list(targets._handle_explicit_target(options, target))
        expected = [TemplateTarget(TEMPLATE, CONFIGURATION, OUTPUT, "use-me")]
        eq_(expected, actual)

    def test_derive_template_type_from_target_template_file(self):

        target = dict(template=TEMPLATE, output=OUTPUT)
        options = dict(
            configuration=CONFIGURATION,
            template_type=DEFAULT_TEMPLATE_TYPE,
            template_dir=TEMPLATE_DIRS,
        )

        actual = list(targets._handle_explicit_target(options, target))
        expected = [TemplateTarget(TEMPLATE, CONFIGURATION, OUTPUT, "jj2")]
        eq_(expected, actual)

    def test_use_moban_default_template_from_options(self):
        template_without_suffix = "template"
        target = dict(template=template_without_suffix, output=OUTPUT)
        options = dict(
            configuration=CONFIGURATION,
            template_type=DEFAULT_TEMPLATE_TYPE,
            template_dir=TEMPLATE_DIRS,
        )

        actual = list(targets._handle_explicit_target(options, target))
        expected = [
            TemplateTarget(
                template_without_suffix,
                CONFIGURATION,
                OUTPUT,
                DEFAULT_TEMPLATE_TYPE,
            )
        ]
        eq_(expected, actual)

    def test_ad_hoc_type(self):
        target = dict(template=TEMPLATE, output=OUTPUT)
        template_type = [
            {"base_type": "jinja2"},
            {
                "options": [
                    {"block_end_string": "*))"},
                    {"block_start_string": "((*"},
                ]
            },
        ]
        options = dict(
            configuration=CONFIGURATION,
            template_type=template_type,
            template_dir=TEMPLATE_DIRS,
        )

        actual = list(targets._handle_explicit_target(options, target))
        file_extension = uuid.uuid4().hex
        expected = [
            TemplateTarget(TEMPLATE, CONFIGURATION, OUTPUT, file_extension)
        ]
        eq_(actual, expected)
