from moban.core.content_processor import ContentProcessor


@ContentProcessor("de-duplicate", "De-duplicating", "De-duplicated")
def de_duplicate(content: str) -> str:
    """
    Does no templating, works like 'copy'.

    """
    lines = content.split(b"\n")
    new_lines = []
    for line in lines:
        if line not in new_lines:
            new_lines.append(line)
    return b"\n".join(new_lines)
