import os

from moban.copy import ContentForwardEngine
from nose.tools import eq_


class TestContentForwardEngine:
    def setUp(self):
        template_path = os.path.join("tests", "fixtures")
        self.engine = ContentForwardEngine([template_path])

    def test_get_template(self):
        template_content = self.engine.get_template("copier-test01.csv")
        #  remove '\r' for windows
        eq_("test 01\n", template_content.decode("utf-8").replace("\r", ""))

    def test_encoding_of_template(self):
        template_content_ = self.engine.get_template("coala_color.svg")
        with open("tests/fixtures/coala_color.svg", "r") as expected:
            expected = expected.read()
        eq_(expected, template_content_.decode("utf-8").replace("\r", ""))

    def test_get_template_from_string(self):
        test_content = "simply forwarded"
        template_content = self.engine.get_template_from_string(test_content)
        eq_(test_content, template_content)

    def test_apply_template(self):
        test_content = "simply forwarded"
        template_content = self.engine.apply_template(test_content, "not used")
        eq_(test_content, template_content)
