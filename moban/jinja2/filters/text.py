import re

from moban.jinja2.extensions import JinjaFilter


@JinjaFilter()
def split_length(input_line, length):
    start = 0
    limit = length
    line = re.sub(r"\s+", " ", input_line)
    line_length = len(line)
    if line_length <= length:
        yield line
    else:
        while True:
            if " " in line[start : start + limit]:  # noqa
                # go back and find a space
                while limit > 0 and line[start + limit] != " ":
                    limit -= 1
            else:
                # full whole line is single unit
                # so go forward find a space
                while (start + limit) < len(line) and line[
                    start + limit
                ] != " ":
                    limit += 1

            yield line[start : start + limit]  # noqa
            start = start + limit + 1
            limit = length
            if len(line[start:]) < length or start + limit >= len(line):
                break

        yield line[start:]
