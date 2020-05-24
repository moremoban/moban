from moban.core.templater import ContentProcessor


@ContentProcessor("strip", "Stripping", "Stripped")
def strip(content: str) -> str:
    """Works like 'copy', but strip empty spaces before and after"""
    return content.strip()
