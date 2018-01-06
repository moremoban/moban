from moban.filters.github import github_expand
from nose.tools import eq_


def test_github_expand():
    inputs = [
        ['fix `#12`', 'project', 'organisation'],
        ['fix `#13` too', 'project', 'organisation'],
        ['`#14` works', 'project', 'organisation'],
        ['`PR#15` works', 'project', 'organisation'],
        ['`cool#16` works', 'project', 'organisation'],
        ['`microsoft#cool#PR#17` works', 'project', 'organisation'],
        ['`cool##18` also works', 'project', 'organisation']
    ]
    expectations = [
        'fix `#12 <https://github.com/organisation/project/issues/12>`_',
        'fix `#13 <https://github.com/organisation/project/issues/13>`_ too',
        '`#14 <https://github.com/organisation/project/issues/14>`_ works',
        '`#15 <https://github.com/organisation/project/pull/15>`_ works',
        '`cool#16 <https://github.com/organisation/cool/issues/16>`_ works',
        '`cool#17 <https://github.com/microsoft/cool/pull/17>`_ works',
        '`cool#18 <https://github.com/organisation/cool/issues/18>`_ also works'
    ]
    for input_line, expect in zip(inputs, expectations):
        actual = github_expand(*input_line)
        eq_(actual, expect)
