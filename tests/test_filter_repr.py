from moban.filters.repr import repr_function
from nose.tools import eq_


def test_string():
    me = 'abc'
    expected = repr_function(me)
    eq_(expected, "'abc'")


def test_list():
    me = [1, 2, 3]
    expected = repr_function(me)
    eq_(expected, ["'1'", "'2'", "'3'"])
