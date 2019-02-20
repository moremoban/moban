Level 16: group targets by their template type
================================================================================

Since moban version 0.4.0, you can group your targets with their template type.
For example, with `copy` target, you can do the following things:


Here is example moban file for copying::
  
    configuration:
      template_dir:
        - template-sources
    targets:
      - copy:
        - simple.file.copy: file-in-template-sources-folder.txt
        - "misc-1-copying/can-create-folder/if-not-exists.txt": file-in-template-sources-folder.txt
        - "test-dir": dir-for-copying
        - "test-recursive-dir": dir-for-recusive-copying/**

More information is documented in `misc-1-copying-template`.


template copy does:

#. copies any template inside pre-declared template directory to anywhere. moban will create directory if needed.
#. copies any directory to anywhere. If "**" is followed, moban attempts to do recursive copying.


.. note::

   The suffix `.copy` of `simple.file.copy` will be removed.
