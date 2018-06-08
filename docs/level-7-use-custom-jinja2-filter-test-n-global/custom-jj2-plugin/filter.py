import base64
from moban.extensions import JinjaFilter


@JinjaFilter('base64encode')
def base64_encode(string):
    return base64.b64encode(string)
