from moban.extensions import JinjaFilter


@JinjaFilter('repr')
def repr_function(string):
    if isinstance(string, list):
        return ["'{}'".format(str(element)) for element in string]
    else:
        return "'{}'".format(str(string))
