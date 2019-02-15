Level 15: template copying becomes an action plugin in targets
================================================================================

With `.moban.yml`, you can copy templates to your destination. More information
is documented in `misc-1-copying-template`.


Here is example moban file for copying::
  
    configuration:
      template_dir:
        - template-sources
    targets:
      - output: simple.file.copy
        template: file-in-template-sources-folder.txt
        template_type: copy
      - output: "misc-1-copying/can-create-folder/if-not-exists.txt"
        template: file-in-template-sources-folder.txt
        template_type: copy
      - output: "test-dir"
        template: dir-for-copying
        template_type: copy
      - output: "test-recursive-dir"
        template: dir-for-recusive-copying/**
        template_type: copy


template copy does:


#. copies any template inside pre-declared template directory to anywhere. moban will create directory if needed.
#. copies any directory to anywhere. If "**" is followed, moban attempts to do recursive copying.
