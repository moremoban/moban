Level 3: data override
================================================================================

Often, data value changes slightly. `overrides` key is supported in the yaml file


Evaluation
--------------------------------------------------------------------------------

Here is the command to launch it:

.. code-block:: bash

    moban -c data.yaml -t a.template

'a.output' is the generated file::

    ========header============
    
    world
    
    shijie
    
    ========footer============
