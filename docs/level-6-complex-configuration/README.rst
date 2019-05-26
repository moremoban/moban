Level 6: Complex Configuration
================================================================================

On top of level 5, you could have a common template, where data and output change.
In the following example::

    configuration:
      configuration_dir: 'custom-config'
      template_dir:
        - custom-templates
        - cool-templates
        - '.'
      template: a.template
    targets:
      - output: a.output
        configuration: data.yml
      - output: a.output2
        configuration: data2.yml

where `template` under `confiugration` needs a template file, which will be a
default template across `targets`. And in this example, the expand form of
`targets` is illustrated:

    {
        "output": 'an output file',
        "configuration": 'data file',
        "template": "the template file"
    }

.. warning::

   `a.template` could be a symbolic link on Unix/Linux. It will not work if you
   template
   `a symbolic link on Windows <https://github.com/moremoban/moban/issues/117>`_.
   Use symbolic link at your own calculated risk.


Evaluation
--------------------------------------------------------------------------------

Please go to `docs/level-6-complex-configuration` directory.

Here is the command to launch it:

.. code-block:: bash

    moban

'a.output' is the generated file::

    ========header============
    
    world
    
    shijie
    
    this demonstrations jinja2's include statement
    
    ========footer============

`a.output2` is::

    ========header============
    
    world2
    
    shijie
    
    this demonstrations jinja2's include statement
    
    ========footer============
