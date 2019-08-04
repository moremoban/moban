import zipfile

from fs.zipfs import ZipFS, ReadZipFS, WriteZipFS


class EnhancedReadZipFS(ReadZipFS):
    def geturl(self, path, purpose="download"):
        return "zip://%s!/%s" % (self._file, path)


class EnhancedZipFS(ZipFS):
    def __new__(
        cls,
        file,
        write=False,
        compression=zipfile.ZIP_DEFLATED,
        encoding="utf-8",
        temp_fs="temp://__ziptemp__",
    ):
        if write:
            return WriteZipFS(
                file,
                compression=compression,
                encoding=encoding,
                temp_fs=temp_fs,
            )
        else:
            return EnhancedReadZipFS(file, encoding=encoding)
