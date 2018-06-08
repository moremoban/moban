from moban.extensions import JinjaFilter


@JinjaFilter("repr")
def repr_function(string):
    if isinstance(string, list):
        return ["'{0}'".format(str(element)) for element in string]
    else:
        return "'{0}'".format(str(string))
