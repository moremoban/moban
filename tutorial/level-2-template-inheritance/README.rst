Level 2: template inheritance
================================================================================

What's different here is a.template inherits base.jj2, which is located in
templates directory. This is jinja2's standard template inheritance.


Evaluation
--------------------------------------------------------------------------------

Here is the command to launch it:

.. code-block:: bash

    moban -c data.yaml -t a.template

'a.output' is the generated file.
