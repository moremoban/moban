import fs
import fs.path
from moban import utils, file_system


class BufferedWriter(object):
    def __init__(self):
        self.fs_list = {}

    def write_file_out(self, filename, content):
        if "zip://" in filename:
            self.write_file_out_to_zip(filename, content)
        else:
            utils.write_file_out(filename, content)

    def write_file_out_to_zip(self, filename, content):
        zip_file, file_name = file_system.url_split(filename)
        if zip_file not in self.fs_list:
            self.fs_list[zip_file] = fs.open_fs(
                file_system.to_unicode(zip_file), create=True
            )
        base_dirs = fs.path.dirname(file_name)
        if not self.fs_list[zip_file].exists(base_dirs):
            self.fs_list[zip_file].makedirs(base_dirs)
        self.fs_list[zip_file].writebytes(
            file_system.to_unicode(file_name), content
        )

    def close(self):
        for fsx in self.fs_list.values():
            fsx.close()
