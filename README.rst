================================================================================
moban - 模板 Yet another jinja2 cli command for static text generation
================================================================================

.. image:: https://api.travis-ci.org/moremoban/moban.svg?branch=master
   :target: http://travis-ci.org/moremoban/moban

.. image:: https://dev.azure.com/moremoban/moban/_apis/build/status/moremoban.moban
   :target: https://dev.azure.com/moremoban/moban/_build?definitionId=1&_a=summary

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
static text generation. It is used in `pyexcel` and `coala` project to keep documentation
consistent across the documentations of individual libraries.

Our vision is: any template, any data. Our current architecture enables moban
to plugin any python template engine: mako, handlebars, velocity, haml, slim and tornado
and to plugin any data format: json and yaml. Please look at our issues. We have many
more template engines and data format on the road map.

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

.. code-block:: bash

    $ export HELLO="world"
    $ moban "{{HELLO}}"
    Warning: Both data.yml and /.../.moban.cd/data.yml does not exist
    Warning: Attempting to use environment vars as data...
    Templating {{HELLO}}... to moban.output
    Templated 1 file.
    $ cat moban.output 
    world

Or simply

.. code-block:: bash

    $ HELLO="world" moban "{{HELLO}}"

   
A bit formal example:

.. code-block:: bash

	$ moban -c data.yml -t my.template
	$ cat moban.output

Given data.yml as::

    hello: world

and my.template as::

    {{hello}}

moban.output will contain::

    world

Please note that data.yml will take precedence over environment variables.

`the tutorial`_ has more use cases.

.. _the tutorial: http://moban.readthedocs.org/en/latest/#tutorial

	
Usage
================================================================================

.. code-block:: bash


   usage: moban [-h] [-cd CONFIGURATION_DIR] [-c CONFIGURATION]
                [-td [TEMPLATE_DIR [TEMPLATE_DIR ...]]] [-t TEMPLATE] [-o OUTPUT]
                [-f] [-m MOBANFILE]
                [template]

   Yet another jinja2 cli command for static text generation
   
   positional arguments:
     template              string templates

   optional arguments:
     -h, --help            show this help message and exit
     -cd CONFIGURATION_DIR, --configuration_dir CONFIGURATION_DIR
                           the directory for configuration file lookup
     -c CONFIGURATION, --configuration CONFIGURATION
                           the dictionary file. if not present, moban
                           will try to use environment vars as data
     -td [TEMPLATE_DIR [TEMPLATE_DIR ...]], --template_dir [TEMPLATE_DIR [TEMPLATE_DIR ...]]
                           the directories for template file lookup
     -t TEMPLATE, --template TEMPLATE
                           the template file. this overrides any targets
                           defined in a custom moban file
     -o OUTPUT, --output OUTPUT
                           the output file
     --template_type TEMPLATE_TYPE
                           the template type, default is jinja2
     -f                    force moban to template all files despite of
                           .moban.hashes
     --exit-code           tell moban to change exit code                      
     -m MOBANFILE, --mobanfile MOBANFILE
                           custom moban file
   

Exit codes
--------------------------------------------------------------------------------
By default:

- 0 : no error
- 1 : error occured

With `--exit-code`:

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
