import os
import sys
from textwrap import dedent

from mock import patch
from moban.main import main
from nose.tools import eq_
from fs.opener.parse import parse_fs_url
from moban.externals import file_system


def verify_content(file_name, expected):
    with open(file_name, "r") as f:
        content = f.read()
        eq_(content, expected)


def verify_content_with_fs(file_name, expected):
    content = file_system.read_unicode(file_name)
    eq_(content, expected)


def run_moban(args, folder, criterias):
    with patch.object(sys, "argv", args):
        main()
        for output, expected in criterias:
            verify_content(output, expected)
            os.unlink(output)


def run_moban_with_fs(args, folder, criterias):
    with patch.object(sys, "argv", args):
        main()

        for output, expected in criterias:
            verify_content_with_fs(output, expected)
    result = parse_fs_url(output)
    os.unlink(result.resource)  # delete the zip file


class Docs(object):
    def setUp(self):
        self.current = os.getcwd()
        self.base_folder = "docs"

    def tearDown(self):
        if os.path.exists(".moban.hashes"):
            os.unlink(".moban.hashes")
        os.chdir(self.current)

    def run_moban(self, moban_cli, working_directory, assertions):
        os.chdir(os.path.join(self.base_folder, working_directory))
        run_moban(moban_cli, None, assertions)

    def run_moban_with_fs(self, moban_cli, working_directory, assertions):
        os.chdir(os.path.join(self.base_folder, working_directory))
        run_moban_with_fs(moban_cli, None, assertions)


def custom_dedent(long_texts):
    refined = dedent(long_texts)
    if refined.startswith("\n"):
        refined = refined[1:]
    return refined
