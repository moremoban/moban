def split_length(line, length):
    start = 0
    limit = length
    line_length = len(line)
    if line_length < length:
        yield line
    else:
        while True:
            if ' ' in line[start:start+limit]:
                while limit > 0 and line[start+limit] != ' ':
                    limit -= 1
            else:
                # full whole line is single unit
                while (start+limit) < len(line) and line[start+limit] != ' ':
                    limit += 1

            yield line[start:start+limit]
            start = start+limit+1
            limit = length
            if len(line[start:]) < length or start+limit > len(line):
                break

        yield line[start:]
