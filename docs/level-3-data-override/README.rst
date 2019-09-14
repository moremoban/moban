Level 3: data override
================================================================================

What `moban` brings on the table is data inheritance by introducing `overrides`
key word in the yaml file::

    overrides: data.base.yaml
    ....

And `.moban.cd` is the default directory where the base data file can be placed.


Evaluation
--------------------------------------------------------------------------------

Please change directory to `docs/level-3-data-override` directory.

In this example, `data.yaml` overrides `.moban.cd/data.base.yaml`, here is the
command to launch it:

.. code-block:: bash

    moban -c data.yaml -t a.template

'moban.output' is the generated file::

    ========header============
    
    world
    
    shijie
    
    ========footer============


New development
--------------------------------------------------------------------------------

Since verison 0.6.0, `overrides` syntax support two more use cases:

1 override more than one configuration file
*********************************************

For example::

    overrides:
      - config-file-a.yaml
      - config-file-b.yaml

2 override more than one configuration file
********************************************

For example::

    overrides:
      - config-file-a.yaml: keya
      - config-file-b.yaml: keyb
