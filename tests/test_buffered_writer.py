import os

from moban import file_system
from nose.tools import eq_
from moban.buffered_writer import BufferedWriter, write_file_out

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
        content = file_system.read_text(test_file)
        eq_(content, EXPECTED)
        os.unlink(test_file)
        self.writer.close()

    def test_write_a_zip(self):
        test_file = "zip://testout.zip!/testout"
        self.writer.write_file_out(test_file, CONTENT)
        content = file_system.read_text(test_file)
        eq_(content, EXPECTED)
        os.unlink("testout.zip")
        self.writer.close()


def test_write_file_out():
    test_file = "testout"
    write_file_out(test_file, CONTENT)
    with open(test_file, "r") as f:
        content = f.read()
        eq_(content, EXPECTED)
