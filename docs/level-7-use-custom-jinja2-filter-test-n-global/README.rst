Level 7: Custom jinja filters, tests and globals
================================================================================

Level 7 example demonstrates advanced plugin capabilities of moban. The following
moban file had `plugin_dir` specified::

    configuration:
      template_dir:
        - my-templates
      plugin_dir:
        - custom-jj2-plugin
      configuration: data.yml
    targets:
      - filter.output: filter.jj2
      - test.output: test.jj2

Where `custom-jj2-plugin` is a directory holding all jinja2 filters, tests
and globals. Under it, there are 4 files::

    __init__.py     filter.py       test.py     global.py

It is very important to have `__init__.py`, otherwise, it will NOT work. Other three
files are named to show case the feature. You can choose whichever name you prefer,
as long as you and your team could make sense of the names.


Evaluation
--------------------------------------------------------------------------------

Please go to `docs/level-7-use-custom-jinja2-filter-test-n-global` directory,

Here is the command to launch it:

.. code-block:: bash

   $ moban
   Templating filter.jj2 to filter.output
   Templating test.jj2 to test.output
   Templating global.jj2 to global.output
   Templated 3 files.
   Everything is up to date!

Please examine individual template and its associated plugin for more details.
