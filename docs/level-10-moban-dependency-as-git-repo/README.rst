level 10: moban dependency as git repo
================================================================================

.. note::

   You will need to install gitfs2

Since the support to have a pypi package as dependency, the moban pro user will
find it more useful to have git repo so that the changes to static content
could get propagate as it happens using git push and git pull.

For now, github.com, gitlab.com and bitbucket.com are supported. Pull request
is welcome to add or improve this feature.


Here are the sample file::

    configuration:
      template_dir:
        - "git://github.com/moremoban/pypi-mobans.git!/templates"
        - local
      configuration: config.yml
      configuration_dir: "git://github.com/moremoban/pypi-mobans.git!/config"
    targets:
      - mytravis.yml: travis.yml.jj2
      - test.txt: demo.txt.jj2

where `requires` lead to a list of pypi packages. And when you refer to it,
as in level-9 section, please use "pypi-mobans:"


The syntax when submodule exists
--------------------------------------------------------------------------------

The sumodule syntax is::
  
    configuration:
      template_dir:
        - "git://github.com/moremoban/pypi-mobans.git?submodule=true&branch=your_choice_or_default_branch_if_not_specified!/templates"
        - local


If you have reference instead of branch::
  
    configuration:
      template_dir:
        - "git://github.com/moremoban/pypi-mobans.git?submodule=true&reference=your_alternative_reference_but_not_used_together_with_branch!/templates"
        - local

