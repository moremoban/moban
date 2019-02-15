from nose.tools import eq_

from moban.definitions import GitRequire, TemplateTarget


def test_git_require_repr():
    require = GitRequire(git_url="http://github.com/some/repo")
    eq_("http://github.com/some/repo,None,False", repr(require))


def test_template_target_repr():
    require = TemplateTarget("template_file", "dat_file", "output")
    eq_("template_file,dat_file,output,jinja2", repr(require))


def test_template_target_output_suffix_change():
    require = TemplateTarget(
        "template_file", "dat_file", "output.copy", template_type="copy"
    )
    eq_("template_file,dat_file,output,copy", repr(require))


def test_clone_params():
    require = GitRequire(git_url="http://github.com/some/repo")
    actual = require.clone_params()
    expected = {"single_branch": True}
    eq_(expected, actual)


def test_branch_params():
    require = GitRequire(
        git_url="http://github.com/some/repo", branch="ghpages"
    )
    actual = require.clone_params()
    expected = {"single_branch": True, "branch": "ghpages"}
    eq_(expected, actual)
