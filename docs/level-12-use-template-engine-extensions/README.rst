Level 11: use template engine extensions
================================================================================

jinja2 comes with a lot of extensions. In order not to be the blocker in the
middle, **extensions** is allowed in moban file to initialize jinja2 engine
with desired extensions

The extensions syntax is::

   extensions:
     jinja2:
       - jinja2.ext.do
	   - jinja2.ext.loopcontrols


Evaluation
--------------------------------------------------------------------------------

