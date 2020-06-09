class DirectoryNotFound(Exception):
    pass


class FileNotFound(Exception):
    pass


class NoThirdPartyEngine(Exception):
    pass


class MobanfileGrammarException(Exception):
    pass


class NoTemplate(Exception):
    pass


class IncorrectDataInput(Exception):
    pass


class GroupTargetNotFound(Exception):
    pass


class NoGitCommand(Exception):
    pass


class UnsupportedPyFS2Protocol(Exception):
    pass


class NoPermissionsNeeded(Exception):
    pass


class SingleHTTPURLConstraint(Exception):
    pass


class PassOn(Exception):
    """
    Raised when template engine cannot do anything with the given template.

    i.e. given a png image :/
    """

    pass
