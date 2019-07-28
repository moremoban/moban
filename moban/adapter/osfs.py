from fs.osfs import OSFS


class EnhancedOSFS(OSFS):

    def geturl(self, path, purpose="download"):
        # type: (Text, Text) -> Text
        if purpose != "download":
            raise NoURL(path, purpose)
        # file://D:\a\1\s\tests\fixtures\template can be not used by osfs itself.
        return "file://" + self.getsyspath(path).replace('\\', '/')
