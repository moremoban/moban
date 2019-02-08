Level 15: template copying becomes an action plugin in targets
================================================================================

With `.moban.yml`, you can copy templates to your destination. More information
is documented in `misc-1-copying-template`.


Here is example moban file for copying::
  
    configuration:
      template_dir:
        - template-sources
    targets:
      - destination: simple.file.copy
        source: file-in-template-sources-folder.txt
        action: copy
      - destination: "misc-1-copying/can-create-folder/if-not-exists.txt"
        source: file-in-template-sources-folder.txt
        action: copy
      - destination: "test-dir"
        source: dir-for-copying
        action: copy
      - destination: "test-recursive-dir"
        source: dir-for-recusive-copying/**
        action: copy


template copy does:


#. copies any template inside pre-declared template directory to anywhere. moban will
  create directory if needed.
#. copies any directory to anywhere. If "**" is followed, moban attempts to do
   recursive copying.
