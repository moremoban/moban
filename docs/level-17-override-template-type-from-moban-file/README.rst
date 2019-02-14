Level 17: force template type
================================================================================

Since moban version 0.4.0, you can enforce all targets to use one and only one
template type, regardless of their individual template types.


Here is example moban file for copying::
  
    configuration:
      template_dir:
        - template-sources
      force_template_type: copy
    targets:
      - simple.file.copy: file-in-template-sources-folder.txt
      - "misc-1-copying/can-create-folder/if-not-exists.txt": file-in-template-sources-folder.txt
      - "test-dir": dir-for-copying
      - "test-recursive-dir": dir-for-recusive-copying/**

More information is documented in `misc-1-copying-template`.


template copy does:

#. copies any template inside pre-declared template directory to anywhere. moban will create directory if needed.
#. copies any directory to anywhere. If "**" is followed, moban attempts to do recursive copying.
