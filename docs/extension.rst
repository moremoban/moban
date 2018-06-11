Development guide
=======================
                   
Jinja2 extensions for Moban
------------------------------

Since version 0.2, mobanfile supports an extra field `plugin_dir`, along with
`template_dir`. When you put your own jinja2 filters, tests and globals in
your moban repo, you can let moban know about them via this keyword.

Importantly, you have to have `__init__.py` file in your `plugin_dir`. Otherwise,
your plugins will NOT be loaded.

Jinja2 Filter
*******************

.. literalinclude:: ../moban/filters/repr.py


Jinja2 Test
*******************

.. literalinclude:: ../moban/tests/files.py

Jinja2 Globals
*******************

.. literalinclude:: ../tests/test_engine.py
   :lines: 49-61

It is possible to write an installable package including your own jinja2
filters, tests and globals. Please email me for more details.

Template engine extension for Moban
--------------------------------------------------------------------------------

moban version 0.2 started using `lml`_ to employ loose couple plugins. Other
template engines, such as marko, haml can be plugged into moban seamless.

.. image:: engine.png

In order plugin other template engines, it is to write a lml plugin. The following
is an example starting point for any template engine.

.. literalinclude:: ../tests/moban-mako/moban_mako/__init__.py

After you will have finished the engine plugin, you can either place it in `plugin_dir`
in order to get it loaded, or make an installable python package. In the latter case,
please refer to `yehua`_: doing that in less than 5 minutes.

.. _lml: http://lml.readthedocs.io
.. _yehua: http://yehua.readthedocs.io
