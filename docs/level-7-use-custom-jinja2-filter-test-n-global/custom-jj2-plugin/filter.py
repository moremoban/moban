import sys
import base64

from moban.jinja2.extensions import JinjaFilter


@JinjaFilter()
def base64encode(string):
    if sys.version_info[0] > 2:
        content = base64.b64encode(string.encode('utf-8'))
        content = content.decode('utf-8')
    else:
        content = base64.b64encode(string)
    return content
