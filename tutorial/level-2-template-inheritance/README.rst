Level 2: template inheritance
================================================================================

Template inheritance is a feature in Jinja2. This example show how it was done.
`a.template` inherits `base.jj2`, which is located in `.moban.td`, the default
template directory. 


Evaluation
--------------------------------------------------------------------------------

`a.template` inherits `.moban.td/base.jj2` and here is the command to launch it:

.. code-block:: bash

    moban -c data.yaml -t a.template

