Level 3: data override
================================================================================

What `moban` bring on the table is data inheritance by introducing `overrides` key word in the yaml file::

    overrides: data.base.yaml
    ....

And `.moban.cd` is the default directory where the base data file can be placed.


Evaluation
--------------------------------------------------------------------------------

In this example, `data.yaml` overrides `.moban.cd/data.base.yaml`, here is the
command to launch it:

.. code-block:: bash

    moban -c data.yaml -t a.template

'a.output' is the generated file::

    ========header============
    
    world
    
    shijie
    
    ========footer============
