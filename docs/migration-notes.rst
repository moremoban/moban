Migrate to 0.6.x
================================================================================

It has been noticed that, this version will fail to template but do a copy, in
the following situation::

   targets:
     index.rst: index.rst

Please note that 0.6.x changed its behavior to do a copy instead of templating.
