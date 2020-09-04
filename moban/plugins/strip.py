from moban.core.content_processor import ContentProcessor


@ContentProcessor("strip", "Stripping", "Stripped")
def strip(content: str, _: dict) -> str:
    """Works like 'copy', but strip empty spaces before and after"""
    return content.strip()
