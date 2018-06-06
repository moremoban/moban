Development guide
=======================

Jinja2 extensions for Moban
------------------------------

Since version 0.2, mobanfile supports an extra field `plugin_dir`, along with
`template_dir`. When you put your own jinja2 filters, tests and globals in
your moban repo, you can let moban know about them via this keyword.

Jinja2 Filter
*******************

.. literalinclude:: ../../moban/filters/repr.py


Jinja2 Test
*******************

.. literalinclude:: ../../moban/tests/files.py

Jinja2 Globals
*******************

.. literalinclude:: ../../tests/test_engine.py
   :lines: 49-61

It is possible to write an installable package including your own jinja2
filters, tests and globals. Please email me for more details.
