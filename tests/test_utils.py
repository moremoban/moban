import os
from shutil import rmtree

from mock import patch
from moban.utils import mkdir_p


def test_mkdir_p():
    test_path = "a/b/c/d"
    mkdir_p(test_path)
    assert os.path.exists(test_path)
    rmtree(test_path)


@patch("subprocess.check_call")
def test_pip_install(fake_check_all):
    import sys
    from moban.deprecated import pip_install

    pip_install(["package1", "package2"])
    fake_check_all.assert_called_with(
        [sys.executable, "-m", "pip", "install", "package1 package2"]
    )
