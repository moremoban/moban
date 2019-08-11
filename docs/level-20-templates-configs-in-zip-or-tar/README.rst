Level 20: templates, files in a zip or tar
================================================================================

On top of level 6, you could have files in a zip or tar.
In the following example::

    configuration:
      configuration_dir: 'tar://custom-config.tar'
      template_dir:
        - zip://templates.zip
        - cool-templates
        - '.'
    targets:
      - output: 'tar://a.tar/a.output'
        configuration: data.yml
        template: template.in.zip.jj2
      - output: 'zip://a.zip/a.output2'
        configuration: data2.yml
        template: subfolder/template.in.zip.jj2

where `template.in.zip.jj2` were loaded from a zip file


Evaluation
--------------------------------------------------------------------------------

Please go to `docs/level-20-templates-configs-in-zip-or-tar` directory.

Here is the command to launch it:

.. code-block:: bash

    moban

'a.output' is the generated file in a.tar::

    ========header============
    
    world
    
    shijie
    
    this demonstrations jinja2's include statement
    
    ========footer============

`a.output2` is in a.zip::

    ========header============
    
    world2
    
    shijie
    
    this demonstrations jinja2's include statement
    
    ========footer============
