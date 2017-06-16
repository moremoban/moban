================================================================================
moban - 模板 Yet another jinja2 cli command for static text generation
================================================================================

.. image:: https://api.travis-ci.org/chfw/moban.svg?branch=master
   :target: http://travis-ci.org/chfw/moban

.. image:: https://codecov.io/github/chfw/moban/coverage.png
    :target: https://codecov.io/github/chfw/moban

.. image:: https://readthedocs.org/projects/moban/badge/?version=latest
    :target: http://moban.readthedocs.org/en/latest/


:Author: C.W.
:Issues: http://github.com/chfw/moban/issues
:License: MIT
:Version: |version|
:Generated: |today|


**moban** brings the high performance template engine (JINJA2) for web into
static text generation.



Installation
================================================================================
You can install it via pip:

.. code-block:: bash

    $ pip install moban


or clone it and install it:

.. code-block:: bash

    $ git clone http://github.com/chfw/moban.git
    $ cd moban
    $ python setup.py install


Quick start
================================================================================

Here is a simple example:

.. code-block:: bash

	$ moban -c data.yml -t my.template
	$ cat moban.output

Given data.yml as::

    hello: world

and my.template as::

    {{hello}}

moban.output will contain::

    world

`the tutorial`_ has more use cases.

.. _the tutorial: http://moban.readthedocs.org/en/latest/#tutorial

	
Usage
================================================================================

usage: moban [-h] [-cd CONFIGURATION_DIR] [-c CONFIGURATION]
             [-td [TEMPLATE_DIR [TEMPLATE_DIR ...]]] [-t TEMPLATE]
             [--template_type TEMPLATE_TYPE] [-o OUTPUT] [-f]

Yet another jinja2 cli command for static text generation


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
* `--template_type TEMPLATE_TYPE`
  the template type, default is jinja2
* `-o OUTPUT, --output OUTPUT`
  the output file
* `-f`
  force moban to template all files despite of .moban.hashes
