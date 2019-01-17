Level 12: use template engine extensions
================================================================================

jinja2 comes with a lot of extensions. In order not to be the blocker in the
middle, **extensions** is allowed in moban file to initialize jinja2 engine
with desired extensions. Two extensions, expression-statement and loop-controls
are enabled by default.

The extensions syntax is::

   extensions:
     template_type:
       - template.engine.specific.extension

For example::

   extensions:
     jinja2:
       - jinja2.ext.i18n

Please also note that the following extensions are included by default:
`jinja2.ext.do`, `jinja2.ext.loopcontrols`


Evaluation
--------------------------------------------------------------------------------
Please go to `docs/level-12-use-template-engine-extensions` directory.

If you notice the file `a.template`, we are using a for loop control. This is
because moban comes with two default extensions loop-controls and
expression-statement.

Now, let us try to use the extension `with`. To do that, we have to enable the
extension in the `.moban.yml` file following the above syntax. Now, the
extension can be used in the jinja2 templates. One such example is shown in the
`b.template` file.
