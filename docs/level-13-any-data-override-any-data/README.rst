Level 13: any data override any data
================================================================================

It's thought that why shall we constrain ourselves on yaml file format. Along
the development path, json file format was added. What about other file formats?

By default yaml, json is supported. Due to the new capability `overrides` key
word can override any supported data format::

    overrides: data.base.json
    ....

or simple use `.json` data instead of `.yaml` data.

Evaluation
--------------------------------------------------------------------------------

Please change directory to `docs/level-13-any-data-override-any-data` directory.

In this example, `child.yaml` overrides `.moban.cd/parent.json`, here is the
command to launch it:

.. code-block:: bash

    moban -c child.yaml -t a.template

'moban.output' is the generated file::

    ========header============

    world from child.yaml

    shijie from parent.json

    ========footer============


And we can try `child.json`, which you can guess, overrides `.moban.cd/parent.yaml`

.. code-block:: bash

    moban -c child.json -t a.template

'moban.output' is the generated file::

   ========header============

   world from child.json

   shijie from parent.yml

   ========footer============
