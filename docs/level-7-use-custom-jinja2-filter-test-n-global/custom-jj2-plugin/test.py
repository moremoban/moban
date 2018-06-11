from moban.extensions import JinjaTest


@JinjaTest('level7')
def level7(value):
    return value == 'level7'
