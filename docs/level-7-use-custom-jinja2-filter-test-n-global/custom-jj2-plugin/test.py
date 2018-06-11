from moban.extensions import JinjaTest


@JinjaTest()
def level7(value):
    return value == 'level7'
