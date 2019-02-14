import os

from nose.tools import eq_

from moban.copy import ContentForwardEngine


class TestContentForwardEngine:
    def setUp(self):
        template_path = os.path.join("tests", "fixtures")
        self.engine = ContentForwardEngine([template_path])

    def test_get_template(self):
        template_content = self.engine.get_template("copier-test01.csv")
        eq_("test 01\n", template_content)

    def test_get_template_from_string(self):
        test_content = "simply forwarded"
        template_content = self.engine.get_template_from_string(test_content)
        eq_(test_content, template_content)

    def test_apply_template(self):
        test_content = "simply forwarded"
        template_content = self.engine.apply_template(test_content, "not used")
        eq_(test_content, template_content)
