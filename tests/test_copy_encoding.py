import os

from moban.copy import ContentForwardEngine
from nose.tools import eq_


class TestCopyEncoding:
    def setUp(self):
        template_path = os.path.join("tests", "fixtures")
        self.engine = ContentForwardEngine([template_path])

    def test_encoding_of_template(self):
        template_content = self.engine.get_template("coala_color.svg")
        with open("tests/fixtures/coala_color.svg", "rb") as expected:
            expected = expected.read()
        eq_(expected, template_content)
        template_content = self.engine.get_template("non-unicode.char")
        with open("tests/fixtures/non-unicode.char", "rb") as expected:
            expected = expected.read()
        eq_(expected, template_content)
