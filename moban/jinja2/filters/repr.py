from moban.jinja2.extensions import JinjaFilter


@JinjaFilter()
def repr(string):
    if isinstance(string, list):
        return ["'{0}'".format(str(element)) for element in string]
    else:
        return "'{0}'".format(str(string))
