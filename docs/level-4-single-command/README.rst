Level 4: single command
================================================================================

If you use moban regularly and operates over a number of files, you may consider
write a `.moban.yml`, which is a mini script file that commands `moban` to
iterate through a number of files


Evaluation
--------------------------------------------------------------------------------

Please go to `docs/level-4-single-command` directory.


Here is the `.moban.yml`, which replaces the command in level 3::

    targets:
      - a.output: a.template


where `targets` should lead an array of dictionaries.

Here is how to launch it
.. code-block:: bash

    moban

'a.output' is the generated file::

    ========header============
    
    world
    
    shijie
    
    ========footer============
