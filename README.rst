================================================================================
moban - 模板 Yet another jinja2 cli command for static text generation
================================================================================

.. image:: https://api.travis-ci.org/moremoban/moban.svg?branch=master
   :target: http://travis-ci.org/moremoban/moban

.. image:: https://codecov.io/gh/moremoban/moban/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/moremoban/moban

.. image:: https://readthedocs.org/projects/moban/badge/?version=latest
    :target: http://moban.readthedocs.org/en/latest/

.. image:: https://img.shields.io/gitter/room/gitterHQ/gitter.svg
   :target: https://gitter.im/chfw_moban/Lobby

:Author: C.W.
:Issues: http://github.com/moremoban/moban/issues
:License: MIT
:Version: |version|
:Generated: |today|


**moban** brings the high performance template engine (JINJA2) for web into
static text generation. It is used in pyexcel project to keep documentation
consistent across the documentations of individual libraries.


Installation
================================================================================
You can install it via pip:

.. code-block:: bash

    $ pip install moban


or clone it and install it:

.. code-block:: bash

    $ git clone http://github.com/moremoban/moban.git
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

::


   usage: moban [-h] [-cd CONFIGURATION_DIR] [-c CONFIGURATION]
                [-td [TEMPLATE_DIR [TEMPLATE_DIR ...]]] [-t TEMPLATE] [-o OUTPUT]
                [-f] [-m MOBANFILE]
   
   Yet another jinja2 cli command for static text generation
   
   optional arguments:
     -h, --help            show this help message and exit
     -cd CONFIGURATION_DIR, --configuration_dir CONFIGURATION_DIR
                           the directory for configuration file lookup
     -c CONFIGURATION, --configuration CONFIGURATION
                           the dictionary file
     -td [TEMPLATE_DIR [TEMPLATE_DIR ...]], --template_dir [TEMPLATE_DIR [TEMPLATE_DIR ...]]
                           the directories for template file lookup
     -t TEMPLATE, --template TEMPLATE
                           the template file
     -o OUTPUT, --output OUTPUT
                           the output file
     --template_type TEMPLATE_TYPE
                           the template type, default is jinja2
     -f                    force moban to template all files despite of
                           .moban.hashes
     -m MOBANFILE, --mobanfile MOBANFILE
                           custom moban file
   

exit codes
--------------------------------------------------------------------------------

- 0 : no changes
- 1 : has changes
- 2 : error occured

Built-in Filters
================================================================================

split_length
--------------------------------------------------------------------------------

It breaks down the given string into a fixed length paragraph. Here is the syntax::

    {% for line in your_string | split_length(your_line_with) %}
    {{line}}
    {% endfor %}

It is used to keep changelog formatted in
`CHANGELOG.rst.jjs in pypi-mobans project <https://github.com/moremoban/pypi-mobans/blob/master/templates/CHANGELOG.rst.jj2#L15>`_

github_expand
--------------------------------------------------------------------------------

It expands simple hashtags into github issues. Here is the syntax::

    {{ your_github_string | github_expand }}


It makes it easy to mention github reference in change log in all projects. Here is
the place it is applied:
`CHANGELOG.rst.jjs in pypi-mobans project <https://github.com/moremoban/pypi-mobans/blob/master/templates/CHANGELOG.rst.jj2#L15>`_


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

`exists`
--------------------------------------------------------------------------------

Test if a file exists or not
