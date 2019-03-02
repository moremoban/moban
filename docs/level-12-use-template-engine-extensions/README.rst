Level 12: use template engine extensions
================================================================================

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
