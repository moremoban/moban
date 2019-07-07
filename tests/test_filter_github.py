from nose.tools import eq_
from moban.jinja2.filters.github import github_expand


def test_github_expand():
    inputs = [
        ["fix `#12`", "project", "organisation"],
        ["fix `#13` too", "project", "organisation"],
        ["`#14` works", "project", "organisation"],
        ["`PR#15` works", "project", "organisation"],
        ["`repo#PR#15` works", "project", "organisation"],
        ["`cool#16` works", "project", "organisation"],
        ["`microsoft#cool#PR#17` works", "project", "organisation"],
        ["this `cool##18`", "project", "organisation"],
        ["`goog#cool#19` works", "project", "organisation"],
        ["`twitter#cool#weird#19` works", "project", "organisation"],
        ["wont work", "project", "organisation"],
        ["`wont work either`", "prj", "org"],
        ["some `weird` `case` `#10` is", "prj", "org"],
    ]
    expectations = [
        "fix `#12 <https://github.com/organisation/project/issues/12>`_",
        "fix `#13 <https://github.com/organisation/project/issues/13>`_ too",
        "`#14 <https://github.com/organisation/project/issues/14>`_ works",
        "`#15 <https://github.com/organisation/project/pull/15>`_ works",
        "`repo#15 <https://github.com/organisation/repo/pull/15>`_ works",
        "`cool#16 <https://github.com/organisation/cool/issues/16>`_ works",
        "`cool#17 <https://github.com/microsoft/cool/pull/17>`_ works",
        "this `cool#18 <https://github.com/organisation/cool/issues/18>`_",
        "`goog#19 <https://github.com/organisation/goog/issues/19>`_ works",
        "`cool#19 <https://github.com/twitter/cool/issues/19>`_ works",
        "wont work",
        "`wont work either`",
        "some `weird` `case` `#10 <https://github.com/org/prj/issues/10>`_ is",
    ]
    for input_line, expect in zip(inputs, expectations):
        actual = github_expand(*input_line)
        eq_(actual, expect)
