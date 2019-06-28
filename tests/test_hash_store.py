import os
import sys

from nose import SkipTest
from moban.hashstore import HashStore


class TestHashStore:
    def setUp(self):
        self.source_template = os.path.join("tests", "fixtures", "a.jj2")
        self.fixture = (
            "test.out",
            "test content".encode("utf-8"),
            self.source_template,
        )

    def tearDown(self):
        if os.path.exists(".moban.hashes"):
            os.unlink(".moban.hashes")

    def test_simple_use_case(self):
        hs = HashStore()
        flag = hs.is_file_changed(*self.fixture)
        hs.save_hashes()
        assert flag is True

    def test_dest_file_does_not_exist(self):
        hs = HashStore()
        flag = hs.is_file_changed(*self.fixture)
        hs.save_hashes()
        hs2 = HashStore()
        flag = hs2.is_file_changed(*self.fixture)
        assert flag is True

    def test_dest_file_exist(self):
        hs = HashStore()
        flag = hs.is_file_changed(*self.fixture)
        if flag:
            with open(self.fixture[0], "wb") as f:
                f.write(self.fixture[1])
        hs.save_hashes()
        hs2 = HashStore()
        flag = hs2.is_file_changed(*self.fixture)
        assert flag is False
        hs2.save_hashes()
        os.unlink(self.fixture[0])

    def test_dest_file_changed(self):
        """
        The situation is:

        moban once
        then update the generated file
        moban again, and the generated file should be detected
        and get templated
        """
        hs = HashStore()
        flag = hs.is_file_changed(*self.fixture)
        if flag:
            with open(self.fixture[0], "wb") as f:
                f.write(self.fixture[1])
        hs.save_hashes()
        # no change
        hs2 = HashStore()
        flag = hs2.is_file_changed(*self.fixture)
        assert flag is False
        hs2.save_hashes()
        # now let update the generated file
        hs3 = HashStore()
        with open(self.fixture[0], "w") as f:
            f.write("hey changed")
        flag = hs3.is_file_changed(*self.fixture)
        assert flag is True
        hs3.save_hashes()
        os.unlink(self.fixture[0])

    def test_dest_file_file_permision_changed(self):
        """
        Save as above, but this time,
        the generated file had file permision change
        """
        if sys.platform == "win32":
            raise SkipTest("No file permission check on windows")
        hs = HashStore()
        flag = hs.is_file_changed(*self.fixture)
        if flag:
            with open(self.fixture[0], "wb") as f:
                f.write(self.fixture[1])
        hs.save_hashes()
        # no change
        hs2 = HashStore()
        flag = hs2.is_file_changed(*self.fixture)
        assert flag is False
        hs2.save_hashes()
        # now let change file permision of generated file
        hs3 = HashStore()
        os.chmod(self.fixture[0], 0o766)
        flag = hs3.is_file_changed(*self.fixture)
        assert flag is True
        hs3.save_hashes()
        os.unlink(self.fixture[0])
