from os.path import normcase, normpath


def samefile(file1, file2):
    return normcase(normpath(file1)) == normcase(normpath(file2))
