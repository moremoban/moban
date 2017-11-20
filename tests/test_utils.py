import os
import stat

from nose.tools import raises, eq_
from moban.utils import load_external_engine
from moban.utils import file_permissions_copy
from moban.engine import Engine


@raises(ImportError)
def test_load_external_engine():
    load_external_engine("unknown_template_type")


def test_load_mako_engine():  # fake mako
    module = load_external_engine("mako")
    engine_class = module.get_engine("mako")
    assert engine_class == Engine


def create_file(test_file, permission):
    with open(test_file, 'w') as f:
        f.write('test')

    os.chmod(test_file, permission)


def test_file_permission_copy():
    test_source = 'test_file_permission_copy1'
    test_dest = 'test_file_permission_copy2'
    create_file(test_source, 0o046)
    create_file(test_dest, 0o646)
    file_permissions_copy(test_source, test_dest)
    eq_(stat.S_IMODE(os.lstat(test_source).st_mode),
        stat.S_IMODE(os.lstat(test_dest).st_mode))
    os.unlink(test_source)
    os.unlink(test_dest)
