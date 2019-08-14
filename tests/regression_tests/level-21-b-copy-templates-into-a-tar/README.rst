Level 21-b: template copying from a tar to a tar
================================================================================

In level 15, with `.moban.yml`, you can copy templates to your destination. Now
with similiar moban syntax, let me show how to create a new zip file where
all templates are copied to.

Explicit syntax::

    targets:
      - output: "tar://your.zip/explicit"
        template: template_file
        template_type: copy


Implicit syntax::

    targets:
      - output: "tar://your.zip/implicit"
        template: template_file.copy


Shorthand syntax::

    targets:
      - "tar://your.zip/shorthand": template_file.copy


No implicit nor short hand syntax for the following directory copying unless
you take a look at `force-template-type`. When you read
`level-17-force-template-type-from-moban-file/README.rst`, you will find
out more.


Directory copying syntax::

 
    targets:
      - output: "tar://your.zip/dest-dir"
        template: source-dir
        template_type: copy
   

Recursive directory copying syntax::


    targets:
      - output: "tar://your.zip/dest-dir"
        template: source-dir/**
        template_type: copy


Evaluation
--------------------------------------------------------------------------------        

Here is example moban file for copying::
  
    configuration:
      template_dir:
        - "tar://template-sources.tar"
    targets:
      - output: "tar://my.tar/simple.file.copy"
        template: file-in-template-sources-folder.txt
        template_type: copy
      - output: "tar://my.tar/target_without_template_type"
        template: file_extension_will_trigger.copy
      - "tar://my.tar/target_in_short_form": as_long_as_this_one_has.copy
      - output: "tar://my.tar/misc-1-copying/can-create-folder/if-not-exists.txt"
        template: file-in-template-sources-folder.txt
        template_type: copy
      - output: "tar://my.tar/test-dir"
        template: dir-for-copying
        template_type: copy
      - output: "tar://my.tar/test-recursive-dir"
        template: dir-for-recusive-copying/**
        template_type: copy


template copy does:


#. copies any template inside pre-declared template directory to anywhere. moban will create directory if needed.
#. copies any directory to anywhere. If "**" is followed, moban attempts to do recursive copying.
