level 9: moban dependency as pypi package
================================================================================

.. note::

   You will need to install pypifs

Why not enable template reuse? Once a template is written somewhere by somebody,
as long as it is good and useful, it is always to reuse it, isn't it? DRY
principle kicks in.

Now with moban, it is possible to package up your mobans/templates
into a pypi package and distribute it to the world of moban.


Here are the sample file::

    configuration:
      template_dir:
        - "pypi://pypi-mobans-pkg/resources/templates"
      configuration: config.yml
      configuration_dir: "pypi://pypi-mobans-pkg/config"
    targets: 
      - mytravis.yml: travis.yml.jj2
      - test.txt: demo.txt.jj2

When you refer to it in configuration section, here is the syntax::

    configuration:
      - template_dir:
        - "pypi://python-package-name/relative-folder-inside-the-package"

Note: when you do not have relative directory::

    configuration:
      template_dir:
        - "pypi://python-package-name"
