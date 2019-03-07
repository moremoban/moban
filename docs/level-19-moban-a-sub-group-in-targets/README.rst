Level 19: select a group target to run
================================================================================

Since moban version 0.4.2, you can select a group target to run.
For example, with `copy` target mixed with normal file list:

  
    configuration:
      template_dir:
        - template-sources
    targets:
      - a.output: a.template.jj2
      - copy:
        - simple.file.copy: file-in-template-sources-folder.txt
        - "misc-1-copying/can-create-folder/if-not-exists.txt": file-in-template-sources-folder.txt
        - "test-dir": dir-for-copying
        - "test-recursive-dir": dir-for-recusive-copying/**

you can do the following things::

    $ moban -g copy

