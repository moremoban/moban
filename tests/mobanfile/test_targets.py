import os

from nose.tools import eq_

from moban.mobanfile import targets
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
