from nose.tools import eq_
from moban.jinja2.filters.text import split_length


def test_split_length():
    inputs = [
        ["some good issues are helping the developer for the", 12],
        ["http://github.com/chfw/abc is cool", 12],
        ["http://github.com/chfw/abc is cool", 100],
        ["some  extra     space will be     removed", 10],
    ]
    expectations = [
        ["some good", "issues are", "helping the", "developer", "for the"],
        ["http://github.com/chfw/abc", "is cool"],
        ["http://github.com/chfw/abc is cool"],
        ["some extra", "space will", "be removed"],
    ]
    for test, expect in zip(inputs, expectations):
        actual = split_length(*test)
        eq_(list(actual), expect)
