================================================================================
moban - Yet another jinja2 cli command for static text generation
================================================================================

.. image:: https://api.travis-ci.org/chfw/moban.svg?branch=master
   :target: http://travis-ci.org/chfw/moban

.. image:: https://codecov.io/github/chfw/moban/coverage.png
    :target: https://codecov.io/github/chfw/moban

**moban** brings the high performance template engine (JINJA2) for web into
static file generation.


Simple Example
================================================================================

Here is a simple example:

.. code-block:: bash

	$ moban -c data.yaml -t my.template
	$ cat a.output

Given data.yaml as::

    hello: world

and my.template as::

    {{hello}}

a.output will contain::

    world


Usage
================================================================================

usage: moban [-h] [-cd CONFIGURATION_DIR] [-c CONFIGURATION]
             [-td [TEMPLATE_DIR [TEMPLATE_DIR ...]]] [-t TEMPLATE]
             [-o OUTPUT]

optional arguments
--------------------------------------------------------------------------------

* `-h, --help`
  show this help message and exit
* `-cd CONFIGURATION_DIR --configuration_dir CONFIGURATION_DIR`
  the directory for configuration file lookup
* `-c CONFIGURATION, --configuration CONFIGURATION`
  the dictionary file
* `-td [TEMPLATE_DIR [TEMPLATE_DIR ...]], --template_dir [TEMPLATE_DIR [TEMPLATE_DIR ...]]`
  the directories for template file lookup
* `-t TEMPLATE, --template TEMPLATE`
  the template file
* `-o OUTPUT, --output OUTPUT`
  the output file
