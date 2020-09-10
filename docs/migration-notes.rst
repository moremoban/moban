Migrate to 0.8.x
================================================================================

In version 0.8.0, `moban.plugins.jinja2.tests.files` is moved to moban-ansible
package. `moban.plugins.jinja2.filters.github` is moved to moban-jinja2-github
package Please install them for backward compatibility.


Migrate to 0.7.x
================================================================================

From 2020 onwards, minimum requirement is Python 3.6


For existing moban users, python 2 support has been dropped. Please stay with
versions lower than 0.7.0 if you are still using python 2.

Migrate to 0.6.x
================================================================================

It has been noticed that, this version will fail to template but do a copy, in
the following situation::

   targets:
     index.rst: index.rst

Please note that 0.6.x changed its behavior to do a copy instead of templating.
