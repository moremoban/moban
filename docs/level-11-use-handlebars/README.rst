Level 11: use handlebars
================================================================================

moban is extensible via lml. Charlie Liu through google code in 2018 has
kindly contributed moban-handlebars plugin.


Evaluation
--------------------------------------------------------------------------------

Please go to `docs/level-11-use-handlebars` directory.


Here is the `.moban.yml`, whihc replaces the command in level 3::

   requires:
     - moban-handlebars
   
   targets:
     - a.output: a.template.handlebars
     - b.output: base.hbs


where `targets` should lead an array of dictionaries, `requires` installs
moban-handlebars extension. You can provide file suffixes: ".handlebars"
or ".hbs" to your handlebars template.

Here is how to launch it
.. code-block:: bash

    moban
