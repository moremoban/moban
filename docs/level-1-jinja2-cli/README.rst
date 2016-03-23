Level 1 Jinja2 on command line
================================================================================

`moban` reads data in yaml format, renders a template file in jinja2 format and
outputs it to `moban.output`. By default, it looks for `data.yml` as its data file

Evaluation
--------------------------------------------------------------------------------

If you have checked out `level files <https://github.com/chfw/moban/tree/master/tutorial/level-1-jinja2-cli>`_, here are different commands to evaluate it:


.. code-block:: bash

    moban -c data.yml -t a.template

'moban.output' is the generated file.

.. code-block:: bash

    moban -c data.yml -t a.template -o my.output

`-o my.output` will override the default name


.. note::
    You may simply type the short form:
    
    .. code-block:: bash
    
        moban -t a.template
    
    because moban looks for `data.yml` by default
