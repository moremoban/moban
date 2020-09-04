================================================================================
mó bǎn - 模板 General purpose static text generator
================================================================================

.. image:: https://raw.githubusercontent.com/pyexcel/pyexcel.github.io/master/images/patreon.png
   :target: https://www.patreon.com/chfw

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


Announcement
================================================================================


In version 0.8.0, `moban.plugins.jinja2.tests.files` is moved to moban-ansible
package. `moban.plugins.jinja2.filters.github` is moved to moban-jinja2-github
package Please install them for backward compatibility.


From 2020 onwards, minimum requirement is Python 3.6


For existing moban users, python 2 support has been dropped. Please stay with
versions lower than 0.7.0 if you are still using python 2.




Quick start
================================================================================


.. code-block:: bash

    $ export HELLO="world"
    $ moban "{{HELLO}}"
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
    world

Given data.yml as:

.. code-block:: bash

    hello: world

and my.template as:



.. code-block:: bash

    {{hello}}



Please note that data.yml will take precedence over environment variables.

Template inheritance and custom template directories
-------------------------------------------------------

Suppose there exists `shared/base.jj2`, and two templates `child1.jj2` and
`child2.jj2` derives from it. You can do:

.. code-block:: bash

    $ moban -t child1.jj2 -td shared -o child1
    $ moban -t child2.jj2 -td shared -o child2

Data overload and custom data directories
---------------------------------------------

Effectively each data file you give to moban, it overrides environment variables.
Still you can have different layers of data. For example, you can have
`shared/company_info.yml`,  use `project1.yml` for project 1 and
`project2.yml` for project 2. In each of the derived data file, simply mention:

.. code-block:: bash

   overrides: company_info.yml
   ...

Here is the command line to use your data:

.. code-block:: bash

   $ moban -cd shared -c project1.yaml -t README.jj2

Custom jinja2 extension
---------------------------

moban allows the injection of user preferred jinja2 extensions:

.. code-block:: bash

   $ moban -e jj2=jinja2_time.TimeExtension ...

Can I write my own jinja2 test, filter and/or globals
-----------------------------------------------------------

moban allows the freedom of craftsmanship. Please refer to the docs for more
details. Here is an example:

.. code-block:: python

   import sys
   import base64
   
   from moban.plugins.jinja2.extensions import JinjaFilter
   
   
   @JinjaFilter()
   def base64encode(string):
       if sys.version_info[0] > 2:
           content = base64.b64encode(string.encode("utf-8"))
           content = content.decode("utf-8")
       else:
           content = base64.b64encode(string)
       return content

And you can use it within your jinja2 template, `mytest.jj2`:



.. code-block:: python

      {{ 'abc' | base64encode }}


Assume that the custom example was saved in `custom-jj2-plugin`

.. code-block:: bash

   $ moban -pd custom-jj2-plugin -t mytest.jj2 ...

Moban will then load your custom jinja2 functions

Slim template syntax for jinja2
---------------------------------

with `moban-slim <https://github.com/moremoban/moban-slim>`_ installed,

Given a data.json file with the following content

.. code-block::

    {
      "person": {
        "firstname": "Smith",
        "lastname": "Jones",
      },
    }

.. code-block:: bash


   $ moban --template-type slim -c data.json  "{{person.firstname}} {{person.lastname}}"
   Smith Jones

Handlebars.js template
----------------------------

With `moban-handlebars <https://github.com/moremoban/moban-handlebars>`_
installed,

Given a data.json file with the following content

.. code-block::

    {
      "person": {
        "firstname": "Yehuda",
        "lastname": "Katz",
      },
    }


.. code-block:: bash


   $ moban --template-type handlebars -c data.json  "{{person.firstname}} {{person.lastname}}"
   Yehuda Katz

For `handlebars.js` users, yes, the example was copied from handlebarjs.com. The
aim is to show off what we can do.

Let's continue with a bit more fancy feature:



.. code-block:: bash

   $ moban --template-type handlebars -c data.json "{{#with person}}{{firstname}} {{lastname}} {{/with}}"


Moban's way of `pybar3 usage <https://github.com/wbond/pybars3#usage>`_:

Let's save the following file a `script.py` under `helper_and_partial` folder:

.. code-block:: python

   from moban_handlebars.api import Helper, register_partial

   register_partial('header', '<h1>People</h1>')


   @Helper('list')
   def _list(this, options, items):
       result = [u'<ul>']
       for thing in items:
           result.append(u'<li>')
           result.extend(options['fn'](thing))
           result.append(u'</li>')
       result.append(u'</ul>')
       return result

And given `data.json` reads as the following:

.. code-block::

   {
       "people":[
           {"name": "Bill", "age": 100},
           {"name": "Bob", "age": 90},
           {"name": "Mark", "age": 25}
       ]
   }

Let's invoke handlebar template:


.. code-block:: bash

   $ moban --template-type hbs -pd helper_and_partial -c data.json "{{>header}}{{#list people}}{{name}} {{age}}{{/list}}"
   Handlebars-ing {{>header}... to moban.output
   Handlebarsed 1 file.
   $ cat moban.output
   <h1>People</h1><ul><li>Bill 100</li><li>Bob 90</li><li>Mark 25</li></ul>


Velocity template
----------------------------

With `moban-velocity <https://github.com/moremoban/moban-velocity>`_
installed,

Given the following data.json:

.. code-block::

   {"people":
       [
           {"name": "Bill", "age": 100},
           {"name": "Bob", "age": 90},
           {"name": "Mark", "age": 25}
       ]
   }

And given the following velocity.template:

.. code-block::

   Old people:
   #foreach ($person in $people)
    #if($person.age > 70)
     $person.name
    #end
   #end
   
   Third person is $people[2].name

**moban** can do the template:

.. code-block:: bash

   $ moban --template-type velocity -c data.json -t velocity.template
   Old people:

   Bill
 
   Bob
 
 
   Third person is Mark



Can I write my own template engine?
--------------------------------------

Yes and please check for `more details <https://github.com/moremoban/moban/tree/dev/tests/regression_tests/level-7-b-template-engine-plugin>`_.

Given the following template type function, and saved in custom-plugin dir:

.. code-block:: python

   from moban.core.content_processor import ContentProcessor
   
   
   @ContentProcessor("de-duplicate", "De-duplicating", "De-duplicated")
   def de_duplicate(content: str, options: dict) -> str:
       lines = content.split(b'\n')
       new_lines = []
       for line in lines:
           if line not in new_lines:
               new_lines.append(line)
       return b'\n'.join(new_lines)


You can start using it like this:

.. code-block:: bash

   $ moban --template-type de-duplicate -pd custom-plugin -t duplicated_content.txt


TOML data format
----------------------

`moban-anyconfig <https://github.com/moremoban/moban-anyconfig>`_ should be installed first.

Given the following toml file, sample.toml:

.. code-block::

   title = "TOML Example"
   [owner]
   name = "Tom Preston-Werner"


You can do:


.. code-block:: bash

   $ moban -c sample.toml "{{owner.name}} made {{title}}"
   Tom Preston-Werner made TOML Example

Not limited to toml, you can supply moban with the following data formats:

.. csv-table:: Always supported formats, quoting from python-anyconfig
   :header: "Format", "Type", "Requirement"
   :widths: 15, 10, 40

   JSON, json, ``json`` (standard lib) or ``simplejson``
   Ini-like, ini, ``configparser`` (standard lib)
   Pickle, pickle, ``pickle`` (standard lib)
   XML, xml, ``ElementTree`` (standard lib)
   Java properties, properties, None (native implementation with standard lib)
   B-sh, shellvars, None (native implementation with standard lib)

For any of the following data formats, you elect to install by yourself.

.. csv-table:: Supported formats by pluggable backend modules
   :header: "Format", "Type", "Required backend"
   :widths: 15, 10, 40

   Amazon Ion, ion, ``anyconfig-ion-backend`` 
   BSON, bson, ``anyconfig-bson-backend`` 
   CBOR, cbor, ``anyconfig-cbor-backend``  or ``anyconfig-cbor2-backend`` 
   ConifgObj, configobj, ``anyconfig-configobj-backend`` 
   MessagePack, msgpack, ``anyconfig-msgpack-backend``

Or you could choose to install all:

.. code-block:: bash

   $ pip install moban-anyconfig[all-backends]

**Why not to use python-anyconfig itself, but yet another package?**

moban gives you a promise of any location which `python-anyconfig` does not support.

**Why do it mean 'any location'?**

Thanks to `pyfilesystem 2 <https://github.com/PyFilesystem/pyfilesystem2>`_,
moban is able to read data back from `git repo <https://github.com/moremoban/gitfs2>`_, `pypi <https://github.com/moremoban/pypifs>`_ package, `http(s) <https://github.com/moremoban/httpfs>`_, zip,
tar, ftp, `s3 <https://github.com/PyFilesystem/s3fs>`_ or `you name it <https://www.pyfilesystem.org/page/index-of-filesystems/>`_.


Templates and configuration files over HTTP(S)
================================================================================

`httpfs <https://github.com/moremoban/httpfs>`_ should be installed first.

With httpfs, `moban`_ can access any files over http(s) as its
template or data file:

.. code-block:: bash

    $ moban -t 'https://raw.githubusercontent.com/moremoban/pypi-mobans/dev/templates/_version.py.jj2'\
      -c 'https://raw.githubusercontent.com/moremoban/pypi-mobans/dev/config/data.yml'\
      -o _version.py


.. _moban: https://github.com/moremoban/moban

In an edge case, if github repo's public url is given,
this github repo shall not have sub repos. This library will fail to
translate sub-repo as url. No magic.

Templates and configuration files in a git repo
================================================================================

`gitfs2 <https://github.com/moremoban/gitfs2>`_ is optional since v0.7.0 but was
installed by default since v0.6.1

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


Templates and configuration files in a python package
================================================================================

`pypifs <https://github.com/moremoban/pypifs>`_ is optional since v0.7.0 but
was installed by default since v0.6.1

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



Where the configuration sits in a s3 bucket, the output is a file in a zip. The content of s3data.yaml is:


.. code-block:

    hello: world

So what can I do with it
============================

Here is a list of other usages:

#. `Django Mobans <https://github.com/django-mobans>`_, templates for django, docker etc.
#. `Math Sheets <https://github.com/chfw/math-sheets>`_, generate custom math sheets in pdf


At scale, continous templating for open source projects
================================================================================

.. image:: https://github.com/moremoban/moban/raw/dev/docs/images/moban-in-pyexcel-demo.gif

**moban** enabled **continuous templating** in `pyexcel <https://github.com/pyexcel/pyexcel>`_ and
`coala <https://github.com//coala/coala>`_ project to keep
documentation consistent across the documentations of individual libraries in the same
organisation. Here is the primary use case of moban, as of now:

.. image:: https://github.com/moremoban/yehua/raw/dev/docs/source/_static/yehua-story.png
   :width: 600px


Usage beyond command line
=============================

All use cases are `documented <http://moban.readthedocs.org/en/latest/#tutorial>`_

Support
================================================================================

If you like moban, please support me on github,
`patreon <https://www.patreon.com/bePatron?u=5537627>`_
or `bounty source <https://salt.bountysource.com/teams/chfw-pyexcel>`_ to maintain
the project and develop it further.

With your financial support, I will be able to invest
a little bit more time in coding, documentation and writing interesting extensions.

Vision
================================================================================

Any template, any data in any location

**moban** started with bringing the high performance template engine (JINJA2) for web
into static text generation.

**moban** can use other python template engine: mako, handlebars, velocity,
haml, slim and tornado, can read other data format: json and yaml, and can access both
template file and configuration file in
any location: zip, git, pypi package, s3, etc.


Credit
================================================================================

`jinja2-fsloader <https://github.com/althonos/jinja2-fsloader>`_ is the key component to enable PyFilesystem2 support in moban
v0.6x. Please show your stars there too!


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


CLI documentation
================================================================================

.. code-block:: bash

    usage: moban [-h] [-c CONFIGURATION] [-t TEMPLATE] [-o OUTPUT]
                 [-td [TEMPLATE_DIR [TEMPLATE_DIR ...]]]
                 [-pd [PLUGIN_DIR [PLUGIN_DIR ...]]] [-cd CONFIGURATION_DIR]
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
      -pd [PLUGIN_DIR [PLUGIN_DIR ...]], --plugin_dir [PLUGIN_DIR [PLUGIN_DIR ...]]
                            add more directories for plugin lookup
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

      --exit-code           by default, exist code 0 means no error, 1 means error
                            occured. It tells moban to change 1 for changes, 2 for
                            error occured
      -V, --version         show program's version number and exit
      -v                    show verbose, try -v, -vv, -vvv
