level 10: moban dependency as git repo
================================================================================

Since the support to have a pypi package as dependency, the pro user of moban
find it more useful to have git repo so that the changes to static content
could get propagate as it happens using git push and git pull.

For now, github.com, gitlab.com and bitbucket.com are supported. Pull request
is welcome to add or improve this feature.


Here are the sample file::

    requires:
       - https://github.com/moremoban/pypi-mobans
    configuration:
      template_dir:
        - "pypi-mobans:templates"
        - local
      configuration: config.yml
    targets:
      - mytravis.yml: travis.yml.jj2
      - test.txt: demo.txt.jj2

where `requires` lead to a list of pypi packages. And when you refer to it,
please use "pypi-mobans:"