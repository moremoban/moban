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

split_length
--------------------------------------------------------------------------------

It breaks down the given string into a fixed length paragraph. Here is the syntax::

    {% for line in your_string | split_length(your_line_with) %}
    {{line}}
    {% endfor %}

It is used to keep changelog formatted in
`CHANGELOG.rst.jj2 in pypi-mobans project <https://github.com/moremoban/pypi-mobans/blob/master/templates/CHANGELOG.rst.jj2#L15>`_

github_expand
--------------------------------------------------------------------------------

It expands simple hashtags into github issues. Here is the syntax::

    {{ your_github_string | github_expand }}


It makes it easy to mention github reference in change log in all projects. Here is
the place it is applied:
`CHANGELOG.rst.jj2 in pypi-mobans project <https://github.com/moremoban/pypi-mobans/blob/master/templates/CHANGELOG.rst.jj2#L15>`_


Here is Grammar in the changelog.yml::

    =============== ==============================
    Syntax          Meaning
    =============== ==============================
    `#1`            moban issues 1
    `PR#1`          moban pull request 1
    `pyexcel#1`     other project issues 1
    `pyexcel#PR#1`  other project pulll request 1
    =============== ==============================

More details can be found in `moban's changelog.yml <https://github.com/moremoban/moban/blob/master/.moban.cd/changelog.yml#L10>`_

`repr`
--------------------------------------------------------------------------------

Returns a single quoted string in the templated file


Built-in Tests
================================================================================

Jinja2 Test
*******************

.. literalinclude:: ../moban/tests/files.py


`exists`
--------------------------------------------------------------------------------

Test if a file exists or not

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

.. image:: images/engine.svg

In order plugin other template engines, it is to write a lml plugin. The following
is an example starting point for any template engine.

.. code::

   @PluginInfo(
       constants.TEMPLATE_ENGINE_EXTENSION, tags=["file", "extensions", "for", "your", "template"]
   )
   class Engine(object):
       def __init__(self, template_fs, options=None):
           """
           A list template directories will be given to your engine class
           """
   
       def get_template(self, template_file):
           """
           Given a relative path to your template file, please return a templatable thing that does
           the templating function in next function below
           """
   
       def apply_template(self, template, data, output):
            """
            Given the template object from `get_template` function, and data as python dictionary, 
            and output as intended output file, please return "utf-8" encoded string.
            """


After you will have finished the engine plugin, you can either place it in `plugin_dir`
in order to get it loaded, or make an installable python package. In the latter case,
please refer to `yehua`_: doing that in less than 5 minutes.

.. _lml: http://lml.readthedocs.io
.. _yehua: http://yehua.readthedocs.io
