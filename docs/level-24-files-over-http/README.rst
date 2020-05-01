level 24: templates and configuration files over http(s)
================================================================================

.. note::

   You will need to install httpfs

Why not to take a template off the web? Once a template is written somewhere
by somebody, as long as it is good and useful, it is always to reuse it,
isn't it? DRY principle kicks in.

Now with mobanfile, it is possible to package up your mobans/templates and
configuration files from a HTTP(S) protocol.


Here are the sample file::

   configuration:
     template_dir:
       - "https://raw.githubusercontent.com/moremoban/pypi-mobans/dev/templates/"
       - local
     configuration: config.yml
     configuration_dir: "https://raw.githubusercontent.com/moremoban/pypi-mobans/dev/config/"
   targets:
     - mytravis.yml: travis.yml.jj2
     - test.txt: demo.txt.jj2

When you refer to it in configuration section, here is the syntax::

   configuration:
     template_dir:
       - "https://raw.githubusercontent.com/moremoban/pypi-mobans/dev/templates/"

.. warn::

   The trailing '/' must be there.


Maintenance note
--------------------------------------------------------------------------------

To the maintainer, in order to eat the dog food. Please checkout pypi-mobans
and run a http server inside local pypi-mobans folder.

Then update moban's mobanfile to::

   configuration:
     template_dir:
       - "http://localhost:8000/templates/"
       - "http://localhost:8000/statics/"
       - ".moban.d"

Then run `make update`

