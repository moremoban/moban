Level 21: template copying from a zip to a zip
================================================================================

In level 15, with `.moban.yml`, you can copy templates to your destination. Now
with similiar moban syntax, let me show how to create a new zip file where
all templates are copied to.

Explicit syntax::

    targets:
      - output: "zip://your.zip/explicit"
        template: template_file
        template_type: copy


Implicit syntax::

    targets:
      - output: "zip://your.zip/implicit"
        template: template_file.copy


Shorthand syntax::

    targets:
      - "zip://your.zip/shorthand": template_file.copy


No implicit nor short hand syntax for the following directory copying unless
you take a look at `force-template-type`. When you read
`level-17-force-template-type-from-moban-file/README.rst`, you will find
out more.


Directory copying syntax::

 
    targets:
      - output: "zip://your.zip/dest-dir"
        template: source-dir
        template_type: copy
   

Recursive directory copying syntax::


    targets:
      - output: "zip://your.zip/dest-dir"
        template: source-dir/**
        template_type: copy


Evaluation
--------------------------------------------------------------------------------        

Here is example moban file for copying::
  
    configuration:
      template_dir:
        - "zip://template-sources.zip"
    targets:
      - output: "zip://my.zip/simple.file.copy"
        template: file-in-template-sources-folder.txt
        template_type: copy
      - output: "zip://my.zip/target_without_template_type"
        template: file_extension_will_trigger.copy
      - "zip://my.zip/target_in_short_form": as_long_as_this_one_has.copy
      - output: "zip://my.zip/misc-1-copying/can-create-folder/if-not-exists.txt"
        template: file-in-template-sources-folder.txt
        template_type: copy
      - output: "zip://my.zip/test-dir"
        template: dir-for-copying
        template_type: copy
      - output: "zip://my.zip/test-recursive-dir"
        template: dir-for-recusive-copying/**
        template_type: copy


template copy does:


#. copies any template inside pre-declared template directory to anywhere. moban will create directory if needed.
#. copies any directory to anywhere. If "**" is followed, moban attempts to do recursive copying.
