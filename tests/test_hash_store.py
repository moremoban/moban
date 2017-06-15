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
            with open(self.fixture[0], 'w') as f:
                f.write(self.fixture[1])
        hs.close()
        hs2 = HashStore()
        flag = hs2.is_file_changed(*self.fixture)
        assert flag is False
        hs2.close()
        os.unlink(self.fixture[0])
