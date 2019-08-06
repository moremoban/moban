import platform
import fs
from fs.osfs import OSFS
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

_WINDOWS_PLATFORM = platform.system() == "Windows"


class EnhancedOSFS(OSFS):
    def geturl(self, path, purpose="download"):
        if purpose != "download":
            raise fs.errors.NoURL(path, purpose)

        sys_path = self.getsyspath(path)
        if _WINDOWS_PLATFORM and ':' in sys_path:
            drive_letter, path = sys_path.split(':', 1)
            path = path.replace("\\", "/")
            path = quote(path)
            url_path = "{}:{}".format(drive_letter, path)
        else:
            sys_path = sys_path.replace("\\", "/")
            url_path = quote(sys_path)
        return "file://" + url_path
