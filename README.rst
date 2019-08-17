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
static text generation. It is used in `pyexcel` and `coala` project to keep
documentation consistent across the documentations of individual libraries.

Our vision is: any template, any data in any location. Our current architecture
enables moban to plugin any python template engine: mako, handlebars, velocity,
haml, slim and tornado, to plugin any data format: json and yaml, and in
any location: zip, git, pypi package, s3, etc. Please
look at our issues. We have many more template engines and data format on the
road map.


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

Work with files in a git repo
================================================================================

Please install gitfs2::

    $ pip install gitfs2


And then you can do the following:

.. code-block:: bash

    $ moban -t 'git://github.com/moremoban/pypi-mobans.git!/templates/_version.py.jj2' \
            -c 'git://github.com/moremoban/pypi-mobans.git!/config/data.yml' \
            -o _version.py
    Info: Found repo in /Users/jaska/Library/Caches/gitfs2/repos/pypi-mobans
    Templating git://github.com/moremoban/pypi-mobans.git!/templates/_version.py.jj2 to _version.py
    Templated 1 file.
    $ cat _version.py
    __version__ = "0.1.1rc3"
    __author__ = "C.W."


Work with files in a python package
================================================================================

Please install pypifs::

    $ pip install pypifs


And then you can do the following:

.. code-block:: bash

    $ moban -t 'pypi://pypi-mobans-pkg/resources/templates/_version.py.jj2' \
            -c 'pypi://pypi-mobans-pkg/resources/config/data.yml' \
            -o _version.py
    Collecting pypi-mobans-pkg
    ....
    Installing collected packages: pypi-mobans-pkg
    Successfully installed pypi-mobans-pkg-0.0.7
    Templating pypi://pypi-mobans-pkg/resources/templates/_version.py.jj2 to _version.py
    Templated 1 file.
    $ cat _version.py
    __version__ = "0.1.1rc3"
    __author__ = "C.W."

Work with S3 and other cloud based file systems
================================================================================

Please install fs-s3fs::

    $ pip install fs-s3fs

.. code-block:: bash

    $ moban -c s3://${client_id}:${client_secrect}@moremoban/s3data.yml -o 'zip://my.zip!/moban.output' {{hello}}
    $ unzip my.zip
    $ cat moban.output
    world

Where the configuration sits in a s3 bucket, the output is a file in a zip. The content of s3data.yaml is::

    hello: world

	
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

Documentation
=================================================================================

More use cases are documented `here <http://moban.readthedocs.org/en/latest/#tutorial>`_
