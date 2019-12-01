================================================================================
moban - 模板 Any template, any data in any location
================================================================================

.. image:: https://api.travis-ci.org/moremoban/moban.svg?branch=master
   :target: http://travis-ci.org/moremoban/moban

.. image:: https://dev.azure.com/moremoban/moban/_apis/build/status/moremoban.moban
   :target: https://dev.azure.com/moremoban/moban/_build?definitionId=1&_a=summary

.. image:: https://codecov.io/gh/moremoban/moban/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/moremoban/moban

.. image:: https://badge.fury.io/py/moban.svg
   :target: https://pypi.org/project/moban

.. image:: https://pepy.tech/badge/moban
   :target: https://pepy.tech/project/moban

.. image:: https://readthedocs.org/projects/moban/badge/?version=latest
    :target: http://moban.readthedocs.org/en/latest/

.. image:: https://img.shields.io/gitter/room/gitterHQ/gitter.svg
   :target: https://gitter.im/chfw_moban/Lobby

:Author: C.W. and its contributors (See contributors.rst)
:Issues: http://github.com/moremoban/moban/issues
:License: MIT


**moban** started with bringing the high performance template engine (JINJA2) for web
into static text generation. It has been used in `pyexcel` and `coala` project to keep
documentation consistent across the documentations of individual libraries in the same
organisation.

**moban** can use other python template engine: mako, handlebars, velocity,
haml, slim and tornado, can read other data format: json and yaml, and can access both
template file and configuration file in
any location: zip, git, pypi package, s3, etc.

Please look at our issues. We have many more template engines and data format on the
road map.

All use cases are documented `here <http://moban.readthedocs.org/en/latest/#tutorial>`_

Support
================================================================================

If you like moban, please support me on `github <https://github.com/sponsors/chfw>`_,
`patreon <https://www.patreon.com/bePatron?u=5537627>`_
or `bounty source <https://salt.bountysource.com/teams/chfw-pyexcel>`_ to maintain
the project and develop it further.

With your financial support, I will be able to invest
a little bit more time in coding, documentation and writing interesting extensions.


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
    Templating {{HELLO}}... to moban.output
    Templated 1 file.
    $ cat moban.output 
    world

Or

.. code-block:: bash

    $ export HELLO="world"
    $ echo "{{HELLO}}" | moban

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

`gitfs2 <https://github.com/moremoban/gitfs2>`_ is installed by default since v0.6.1


You can do the following with moban:

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

`pypifs <https://github.com/moremoban/pypifs>`_ is installed by default since v0.6.1

You can do the following with moban:

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

Please install `fs-s3fs <https://github.com/PyFilesystem/s3fs>`_::

    $ pip install fs-s3fs


Then you can access your files in s3 bucket:

.. code-block:: bash

    $ moban -c s3://${client_id}:${client_secrect}@moremoban/s3data.yml \
            -o 'zip://my.zip!/moban.output' {{hello}}
    $ unzip my.zip
    $ cat moban.output
    world

Where the configuration sits in a s3 bucket, the output is a file in a zip. The content of s3data.yaml is::

    hello: world
	


CLI documentation
================================================================================

.. code-block:: bash

    usage: moban [-h] [-c CONFIGURATION] [-t TEMPLATE] [-o OUTPUT]
                 [-td [TEMPLATE_DIR [TEMPLATE_DIR ...]]] [-cd CONFIGURATION_DIR]
                 [-m MOBANFILE] [-g GROUP] [--template-type TEMPLATE_TYPE]
                 [-d DEFINE [DEFINE ...]] [-e EXTENSION [EXTENSION ...]] [-f]
                 [--exit-code] [-V] [-v]
                 [template]
    
    Static text generator using any template, any data and any location.
    
    positional arguments:
      template              string templates
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIGURATION, --configuration CONFIGURATION
                            the data file
      -t TEMPLATE, --template TEMPLATE
                            the template file
      -o OUTPUT, --output OUTPUT
                            the output file
    
    Advanced options:
      For better control
    
      -td [TEMPLATE_DIR [TEMPLATE_DIR ...]], --template_dir [TEMPLATE_DIR [TEMPLATE_DIR ...]]
                            add more directories for template file lookup
      -cd CONFIGURATION_DIR, --configuration_dir CONFIGURATION_DIR
                            the directory for configuration file lookup
      -m MOBANFILE, --mobanfile MOBANFILE
                            custom moban file
      -g GROUP, --group GROUP
                            a subset of targets
      --template-type TEMPLATE_TYPE
                            the template type, default is jinja2
      -d DEFINE [DEFINE ...], --define DEFINE [DEFINE ...]
                            to supply additional or override predefined variables,
                            format: VAR=VALUEs
      -e EXTENSION [EXTENSION ...], --extension EXTENSION [EXTENSION ...]
                            to to TEMPLATE_TYPE=EXTENSION_NAME
      -f                    force moban to template all files despite of
                            .moban.hashes
    
    Developer options:
      For debugging and development
    
      --exit-code           tell moban to change exit code
      -V, --version         show program's version number and exit
      -v                    show verbose, try -v, -vv, -vvv

Exit codes
--------------------------------------------------------------------------------
By default:

- 0 : no error
- 1 : error occured

With `--exit-code`:

- 0 : no changes
- 1 : has changes
- 2 : error occured
