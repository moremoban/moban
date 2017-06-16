Level 5: custom configuration
================================================================================

With `.moban.yml`, you can even change default data directory `.moban.cd` and
default template directory `.moan.td`. Read this example::

    configuration:
      configuration_dir: 'custom-config'
      template_dir:
        - custom-templates
        - cool-templates
        - '.'
    targets:
      - a.output: a.template


where `configuration` lead a dictionary of key words:

#. `configuration_dir` - the new configuration directory
#. `template_dir` - an array of template directories


Evaluation
--------------------------------------------------------------------------------

Please go to `docs/level-5-custom-configuration` directory.


Here is the command to launch it:

.. code-block:: bash

    moban

'a.output' is the generated file::

    ========header============
    
    world
    
    shijie
    
    this demonstrations jinja2's include statement
    
    ========footer============
