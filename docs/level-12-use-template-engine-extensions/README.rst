Level 12: use template engine extensions
================================================================================

There are three possible ways to provide extensions for your template engine.
Let's take jinja2 as an example.

1. Ready made extensions
-----------------------------

jinja2 comes with a lot of extensions. In order not to be the blocker in the
middle, **extensions** is allowed in moban file to initialize jinja2 engine
with desired extensions. Two extensions, expression-statement and loop-controls
are enabled by default.

The extensions syntax is::

   extensions:
     template_type:
       - template.engine.specific.extension

For example::

   extensions:
     jinja2:
       - jinja2.ext.i18n

Please also note that the following extensions are included by default:
`jinja2.ext.do`, `jinja2.ext.loopcontrols`


**Command line**

if you intend to use extensions for one off usage, please use '-e' cli option.
for example: `moban -e jinja2=your_custom_jinja2_extension <https://github.com/chfw/math-sheets/blob/master/reception/a_op_b_op_c/make.sh>`_

 
2. Ad-hoc declaration
-----------------------------

Let's say you are fond of some existing functions, for example, ansible's combine
filter. With moban, you can immediately include it for your template via the following
syntax:

.. code-block::

   extensions:
     jinja2:
       - filter:module.path.filter_function
       - test:module.path.test_function
       - global:identifier=module.path.variable

For example::

   extensions:
     jinja2:
       - filter:ansible.plugins.filter.core.combine
       - test:moban.externals.file_system.exists

**Command line**

.. code-block:: bash

   $ moban -e jinja2=filter:module.path.filter_function jinja2=test:module.path.test_function jinja2=global:identifier=module.path.variable

you can do this::

   $ moban -e jinja2=filter:module.path.filter_function \
              jinja2=test:module.path.test_function \
              jinja2=global:identifier=module.path.variable


3. Make your own extensions
--------------------------------

You can choose to write an extension for the template type of your choice.
For example, you can write a reusable extension for jinja2. moban will be
able to load it as it is.

If you decide that you only want to write them for moban but for your own
use, you can follow `Level 7: Custom jinja filters, tests and globals` and
write your own. When you would like to make yours avaiable for all moban
users, you can follow `moban-jinja2-github <https://github.com/moremoban/moban-jinja2-github>`_ and
`moban-ansible <https://github.com/moremoban/moban-ansible>`_ 


Evaluation
--------------------------------------------------------------------------------
Please go to `docs/level-12-use-template-engine-extensions` directory.

If you notice the file `a.template`, we are using a for loop control. This is
because moban comes with two default extensions loop-controls and
expression-statement.

Now, let us try to use the extension `with`. To do that, we have to enable the
extension in the `.moban.yml` file following the above syntax. Now, the
extension can be used in the jinja2 templates. One such example is shown in the
`b.template` file.

.. note::
  
  For some extensions, you may need to define `template environment parameters`.
  In that case, you can take help of our `user defined template types` feature.
  Please read level-18 for more info. We have explained it using an example
  here.

  Let us consider the example of `jinja2_time`. If you want to use
  `datetime_format` attribute, you need to specify the same using environmental
  parameters, *i.e*  `env.datetime_format = '%a, %d %b %Y %H:%M:%S'`. In order
  to do this, you can specify `datetime_format` using environmental parameters,
  something like::

    configuration:
      template_types:
        my_own_type:
          base_type: jinja2
          file_extensions:
            - file_type_of_my_choice
          options:
            datetime_format: %a, %d %b %Y %H:%M:%S
            extensions:
              - jinja2_time.TimeExtension
    targets:
      - a.output: a.template.file_type_of_my_choice
