from functools import wraps

from moban import reporter


def deprecated(message):
    def tags_decorator(func):
        @wraps(func)
        def func_wrapper(*args, **kwds):
            reporter.report_warning_message(message)
            return func(*args, **kwds)

        return func_wrapper

    return tags_decorator
