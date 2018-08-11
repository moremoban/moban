level 9: moban dependency as pypi package
================================================================================

Why not enable template reuse? Once a template is written somewhere by somebody,
as long as it is good and useful, it is always to reuse it, isn't it? DRY
principle kicks in.

Now with moban, it is possible to package up your mobans/templates
into a pypi package and distribute it to the world of moban.


Here are the sample file::

    requires:
       - pypi-mobans
    configuration:
      template_dir:
        - "pypi-mobans:templates"
      configuration: config.yml
    targets: 
      - mytravis.yml: travis.yml.jj2
      - test.txt: demo.txt.jj2

where `requires` lead to a list of pypi packages. And when you refer to it,
please use "pypi-mobans:"
