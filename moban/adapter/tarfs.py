import os

import six
from fs.tarfs import TarFS, ReadTarFS, WriteTarFS


class EnhancedReadTarFS(ReadTarFS):
    def geturl(self, path, purpose="download"):
        return "tar://%s!/%s" % (self._file, path)


class EnhancedTarFS(TarFS):
    def __new__(
        cls,
        file,
        write=False,
        compression=None,
        encoding="utf-8",
        temp_fs="temp://__tartemp__",
    ):
        if isinstance(file, (six.text_type, six.binary_type)):
            file = os.path.expanduser(file)
            filename = file
        else:
            filename = getattr(file, "name", "")

        if write and compression is None:
            compression = None
            for comp, extensions in six.iteritems(cls._compression_formats):
                if filename.endswith(extensions):
                    compression = comp
                    break

        if write:
            return WriteTarFS(
                file,
                compression=compression,
                encoding=encoding,
                temp_fs=temp_fs,
            )
        else:
            return EnhancedReadTarFS(file, encoding=encoding)
