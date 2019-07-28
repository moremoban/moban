import zipfile

from fs.zipfs import ZipFS, ReadZipFS, WriteZipFS


class EnhancedReadZipFS(ReadZipFS):
    def geturl(self, path, purpose="download"):
        return "zip://%s/%s" % (self._file, path)


class EnhancedZipFS(ZipFS):
    def __new__(
        cls,
        file,  # type: Union[Text, BinaryIO]
        write=False,  # type: bool
        compression=zipfile.ZIP_DEFLATED,  # type: int
        encoding="utf-8",  # type: Text
        temp_fs="temp://__ziptemp__",  # type: Text
    ):
        # type: (...) -> FS
        # This magic returns a different class instance based on the
        # value of the ``write`` parameter.
        if write:
            return WriteZipFS(
                file,
                compression=compression,
                encoding=encoding,
                temp_fs=temp_fs,
            )
        else:
            return EnhancedReadZipFS(file, encoding=encoding)
