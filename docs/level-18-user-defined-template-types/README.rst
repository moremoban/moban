Level 18: User defined template types
================================================================================

Since moban version 4.1, custom template types can be defined to deviate from
default configurations of the template engines. In addition, the configuration
possibilities are:

#. associate your own file extensions
#. choose your own template engine extensions


Evaluation
--------------------------------------------------------------------------------

Please go to `docs/level-4-single-command` directory.


Here is the `.moban.yml`, which inserts `template_types` on top of the moban
file found in level 4::

    configuration:
      template_types:
        my_own_type:
          base_type: jinja2
          file_extensions:
            - file_type_of_my_choice
          options:
            extensions:
              - jinja2_time.TimeExtension
    targets:
      - a.output: a.template.file_type_of_my_choice


where `template_types` is a dictionary of different custom types.

Also, you can define your `template` on the fly by putting the template
parameters inside targets. One such example is::

    targets:
      - output: b.output
        template: a.template.jj2
        template_type:
          base_type: jinja2
          options:
            block_end_string: '*))'
            block_start_string: '((*'
            variable_start_string: '((('
            variable_end_string: ')))'
