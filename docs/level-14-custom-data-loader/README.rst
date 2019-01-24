Level 14: custom data loader
================================================================================

Continuing from level 13, `moban` since v0.4.0 allows data loader extension.
Due to the new capability `overrides` key word can override any
data format::

    overrides: yours.custom
    ....

or simple use `.custom` data instead of `.yaml` data.

However, you will need to provide a data loader for `.custom` yourselves.

Evaluation
--------------------------------------------------------------------------------

Please change directory to `docs/level-14-custom-data-loader` directory.


In this tutorial, a custom data loader was provided to show case its dataloader
extension. Here is the mobanfile::

   configuration:
     plugin_dir:
       - custom-data-loader
     template: a.template
   targets:
     - output: a.output
       configuration: child.custom
     - output: b.output
       configuration: override_custom.yaml

`custom-data-loader` is a directory where custom.py lives. The protocol is
that the custom loader register itself to a file extension and return
a data dictionary confirming mobanfile schema. On call, `moban` will provide
an absolute file name for your loader to work on.


Here is the code to do the registration:

.. code-block:: python

   @PluginInfo(constants.DATA_LOADER_EXTENSION, tags=["custom"])


In order to evaluate, you can simply type::

   $ moban
   $ cat a.output
   ========header============

   world from child.cusom

   shijie from parent.json

   ========footer============
   $ cat b.output
   ========header============

   world from override_custom.yaml

   shijie from parent.custom

   ========footer============


.. warning::

   Python 2 dictates the existence of __init__.py in the plugin directory. Otheriwse
   your plugin won't load
