Level 1 Jinja2 on command line
================================================================================

`moban` reads data in yaml format, renders a template file in jinja2 format and
outputs it to `moban.output`. By default, it looks for `data.yml` as its data file,
but it will fallback to environment variables if a data file cannot be found

Evaluation
--------------------------------------------------------------------------------

Please clone the moban project and install moban::


    $ git clone https://github.com/chfw/moban.git
    $ cd moban
    $ python setup.py install


Then go to `docs/level-1-jinja2-cli`. here are different commands to evaluate it:


.. code-block:: bash

    moban -c data.yml -t a.template

'moban.output' is the generated file.

.. code-block:: bash

    moban -c data.yml -t a.template -o my.output

`-o my.output` will override the default name


.. note::
    You may simply type the short form:
    
    .. code-block:: bash
    
        moban -t a.template
    
    because moban looks for `data.yml` by default

As well, you can define your own variable:

.. code-block:: bash

   moban -D hello=maailman -t a.template

And when you check 'moban.output', you will find you have overwritten data.yaml.
