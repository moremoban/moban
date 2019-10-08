import os
import tempfile

from nose.tools import eq_

from moban.externals import file_system
from moban.externals.buffered_writer import BufferedWriter, write_file_out

CONTENT = b"""
    helloworld




    """
EXPECTED = "\n    helloworld\n\n\n\n\n    "


class TestBufferedWriter:
    def setUp(self):
        self.writer = BufferedWriter()

    def test_write_text(self):
        test_file = "testout"
        self.writer.write_file_out(test_file, CONTENT)
        self.writer.close()
        content = file_system.read_text(test_file)
        eq_(content, EXPECTED)
        os.unlink(test_file)

    def test_write_a_zip(self):
        tmp_dir = os.path.normcase(tempfile.gettempdir())
        test_file = "zip://" + tmp_dir + "/testout.zip!/testout"
        self.writer.write_file_out(test_file, CONTENT)
        self.writer.close()
        content = file_system.read_text(test_file)
        eq_(content, EXPECTED)
        os.unlink(os.path.join(tmp_dir, "testout.zip"))


def test_write_file_out():
    test_file = "testout"
    write_file_out(test_file, CONTENT)
    with open(test_file, "r") as f:
        content = f.read()
        eq_(content, EXPECTED)
