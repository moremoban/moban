Level 2: template inheritance
================================================================================

Template inheritance is a feature in Jinja2. This example show how it was done.
`a.template` inherits `base.jj2`, which is located in `.moban.td`, the default
template directory.


.. warning::

   `a.template` could be a symbolic link on Unix/Linux. It will not work if you
   template
   `a symbolic link on Windows <https://github.com/moremoban/moban/issues/117>`_.
   Use symbolic link at your own calculated risk.


Evaluation
--------------------------------------------------------------------------------

Please go to `docs/level-2-template-inheritance`, here is the command to launch it:

.. code-block:: bash

    moban -c data.yaml -t a.template

`a.template` inherits `.moban.td/base.jj2`.
