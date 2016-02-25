================================================================================
moban - 模板 Yet another jinja2 cli command for static text generation
================================================================================

.. image:: https://api.travis-ci.org/chfw/moban.svg?branch=master
   :target: http://travis-ci.org/chfw/moban

.. image:: https://codecov.io/github/chfw/moban/coverage.png
    :target: https://codecov.io/github/chfw/moban

**moban** brings the high performance template engine (JINJA2) for web into
static file generation.


Installation
============
You can install it via pip:

.. code-block:: bash

    $ pip install http://github.com/chfw/moban/archive/master.zip


or clone it and install it:

.. code-block:: bash

    $ git clone http://github.com/chfw/moban.git
    $ cd moban
    $ python setup.py install


Quick start
================================================================================

Here is a simple example:

.. code-block:: bash

	$ moban -c data.yaml -t my.template
	$ cat moban.output

Given data.yaml as::

    hello: world

and my.template as::

    {{hello}}

moban.output will contain::

    world

`the tutorial`_ has more use cases.

.. _the tutorial: tutorial/README.rst

	
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
