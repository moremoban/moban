from moban.jinja2.extensions import JinjaTest


@JinjaTest()
def level7(value):
    return value == 'level7'
