import fs.path
from fs.osfs import OSFS
from moban.plugins.library import LIBRARIES
from fs.opener import Opener
from moban import repo


class PypiFSOpener(Opener):
    protocols = ['pypi']

    def open_fs(self, fs_url, parse_result, writeable, create, cwd):
        pypi_package_name, _, dir_path = parse_result.resource.partition('/')
        library_path = LIBRARIES.resource_path_of(pypi_package_name)
        root_path = fs.path.join(library_path, dir_path)
        osfs = OSFS(
            root_path=root_path
        )
        return osfs


class RepoOpener(Opener):
    protocols = ['repo']

    def open_fs(self, fs_url, parse_result, writeable, create, cwd):
        repo_name, _, dir_path = parse_result.resource.partition('/')
        actual_repo_path = fs.path.join(repo.get_moban_home(), repo_name)
        root_path = fs.path.join(actual_repo_path, dir_path)
        osfs = OSFS(
            root_path=root_path
        )
        return osfs
