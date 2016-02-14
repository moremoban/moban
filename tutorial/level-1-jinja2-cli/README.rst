Level 1 Jinja2 on command line
================================================================================

`moban` takes a data file in yaml and a template file in jinja2 format. And its
output file by default is `moban.output`.

Evaluation
--------------------------------------------------------------------------------

Here is the command to launch it:

.. code-block:: bash

    moban -c data.yml -t a.template

'moban.output' is the generated file.

.. code-block:: bash

    moban -c data.yml -t a.template -o my.output

`-o my.output` will override the default name

You may simply type the short form:

.. code-block:: bash

    moban -t a.template

because moban looks for `data.yml` by default
