from os.path import (
    isabs,
    isdir,
    exists,
    isfile,
    islink,
    ismount,
    lexists,
    samefile,
)

from moban.extensions import jinja_tests

jinja_tests(
    is_dir=isdir,
    directory=isdir,
    is_file=isfile,
    file=isfile,
    is_link=islink,
    link=islink,
    exists=exists,
    link_exists=lexists,
    # path testing
    is_abs=isabs,
    abs=isabs,
    is_same_file=samefile,
    same_file=samefile,
    is_mount=ismount,
    mount=ismount,
)
