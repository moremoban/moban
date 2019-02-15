import os

from mock import patch
from nose.tools import eq_

from moban.mobanfile import targets
from moban.definitions import TemplateTarget


def test_get_explicit_target():
    target = dict(template_type="not-known", template="a.jj2", output="new")
    options = dict(
        configuration="data.config",
        template_type="special",
        template_dir=[os.path.join("tests", "fixtures")],
    )

    actual = list(targets._handle_explicit_target(options, target))
    expected = [TemplateTarget("a.jj2", "data.config", "new", "not-known")]
    eq_(expected, actual)
