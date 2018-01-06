import re

ISSUE = '^.*?`(.*)`.*?$'
SAME_PROJ_FULL_ISSUE = '`#{3} <https://github.com/{0}/{1}/{2}/{3}>`_'
DIFF_PROJ_FULL_ISSUE = '`{1}#{3} <https://github.com/{0}/{1}/{2}/{3}>`_'


def github_expand(line, name, organisation):
    result = re.match(ISSUE, line)
    if result:
        github_thing = result.group(1)
        tokens = github_thing.split('#')
        if len(tokens) == 4:
            if tokens[2] == 'PR':
                tokens[2] = 'pull'
            else:
                tokens[2] = 'issues'
        elif len(tokens) == 3:
            if tokens[1] == 'PR':
                tokens = [organisation, tokens[0], 'pull', tokens[2]]
            else:
                tokens = [organisation, tokens[0], 'issues', tokens[2]]
        elif len(tokens) == 2:
            if tokens[0] == 'PR':
                tokens = [organisation, name, 'pull'] + tokens[1:]
            elif tokens[0] != '':
                tokens = [organisation, tokens[0], 'issues'] + tokens[1:]
            else:
                tokens = [organisation, name, 'issues'] + tokens[1:]
        if tokens[1] != name:
            reference = DIFF_PROJ_FULL_ISSUE.format(*tokens)
        else:
            reference = SAME_PROJ_FULL_ISSUE.format(*tokens)
        return re.sub('`(.*)`', reference, line)
    else:
        return result
