from moban.extensions import JinjaTest


@JinjaTest('level7')
def test_level7(value):
    return value == 'level7'
