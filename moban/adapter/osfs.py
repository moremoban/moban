import fs
from fs.osfs import OSFS


class EnhancedOSFS(OSFS):
    def geturl(self, path, purpose="download"):
        if purpose != "download":
            raise fs.errors.NoURL(path, purpose)
        return "file://" + self.getsyspath(path).replace("\\", "/")
