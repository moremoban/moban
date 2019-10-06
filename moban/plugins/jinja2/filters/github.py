import re

from moban.jinja2.extensions import JinjaFilter

GITHUB_REF_PATTERN = "`([^`]*?#[0-9]+)`"
ISSUE = "^.*?" + GITHUB_REF_PATTERN + ".*?$"
SAME_PROJ_FULL_ISSUE = "`#{3} <https://github.com/{0}/{1}/{2}/{3}>`_"
DIFF_PROJ_FULL_ISSUE = "`{1}#{3} <https://github.com/{0}/{1}/{2}/{3}>`_"
PULL_REQUEST = "PR"
PULL = "pull"
ISSUES = "issues"


@JinjaFilter()
def github_expand(line, name, organisation):
    result = re.match(ISSUE, line)
    if result:
        github_thing = result.group(1)
        tokens = github_thing.split("#")
        if len(tokens) == 4:
            if tokens[2] == PULL_REQUEST:
                tokens[2] = PULL
            else:
                tokens[2] = ISSUES
        elif len(tokens) == 3:
            if tokens[1] == PULL_REQUEST:
                tokens = [organisation, tokens[0], PULL, tokens[2]]
            else:
                tokens = [organisation, tokens[0], ISSUES, tokens[2]]
        elif len(tokens) == 2:
            if tokens[0] == PULL_REQUEST:
                tokens = [organisation, name, PULL] + tokens[1:]
            elif tokens[0] != "":
                tokens = [organisation, tokens[0], ISSUES] + tokens[1:]
            else:
                tokens = [organisation, name, ISSUES] + tokens[1:]
        if tokens[1] != name:
            reference = DIFF_PROJ_FULL_ISSUE.format(*tokens)
        else:
            reference = SAME_PROJ_FULL_ISSUE.format(*tokens)
        return re.sub(GITHUB_REF_PATTERN, reference, line)
    else:
        return line
