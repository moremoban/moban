Level 11: use handlebars
================================================================================

moban is extensible via lml. Charlie Liu through Google Code-in 2018 has
kindly contributed moban-handlebars plugin.


Evaluation
--------------------------------------------------------------------------------

Please go to `docs/level-11-use-handlebars` directory. You will have to::

    $ pip install moban-handlebars


Here is the `.moban.yml`, which replaces `jj2` with handlebars files in level 4::

   targets:
     - a.output: a.template.handlebars
     - b.output: base.hbs


where `targets` should lead an array of dictionaries, `requires` installs
moban-handlebars extension. You can provide file suffixes: ".handlebars"
or ".hbs" to your handlebars template.

Here is how to launch it
.. code-block:: bash

    moban
