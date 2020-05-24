from moban.core.content_processor import ContentProcessor


@ContentProcessor("copy", "Copying", "Copied")
def copy(content: str) -> str:
    """
    Does no templating, works like 'copy'.

    Respects templating directories, for example: naughty.template
    could exist in any of template directires: dir1,
    dir2, dir3, and this engine will find it for you.  With conventional
    copy command, the source file path must be known.

    And this engine does not really touch the dest file but only read
    the source file. Everything else is taken care of by moban
    templating mechanism.
    """
    return content
