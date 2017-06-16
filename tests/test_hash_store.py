import os
from moban.utils import HashStore


class TestHashStore:
    def setUp(self):
        self.fixture = ('test.out', 'test content'.encode('utf-8'))

    def tearDown(self):
        os.unlink('.moban.hashes')

    def test_simple_use_case(self):
        hs = HashStore()
        flag = hs.is_file_changed(*self.fixture)
        assert flag is True
        hs.close()

    def test_dest_file_does_not_exist(self):
        hs = HashStore()
        flag = hs.is_file_changed(*self.fixture)
        hs.close()
        hs2 = HashStore()
        flag = hs2.is_file_changed(*self.fixture)
        assert flag is True
        hs2.close()

    def test_dest_file_exist(self):
        hs = HashStore()
        flag = hs.is_file_changed(*self.fixture)
        if flag:
            with open(self.fixture[0], 'wb') as f:
                f.write(self.fixture[1])
        hs.close()
        hs2 = HashStore()
        flag = hs2.is_file_changed(*self.fixture)
        assert flag is False
        hs2.close()
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
            with open(self.fixture[0], 'wb') as f:
                f.write(self.fixture[1])
        hs.close()
        # no change
        hs2 = HashStore()
        flag = hs2.is_file_changed(*self.fixture)
        assert flag is False
        hs2.close()
        # now let update the generated file
        hs3 = HashStore()
        with open(self.fixture[0], 'wb') as f:
            f.write('hey changed')
        flag = hs3.is_file_changed(*self.fixture)
        assert flag is True
        hs3.close()
        os.unlink(self.fixture[0])
