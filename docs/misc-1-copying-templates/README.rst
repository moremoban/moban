Misc 1: copying templates - Deprecated since version 0.4.0
================================================================================

.. warning::
   This chapter is kept for regression testing. If you have moban v0.4.0 or
   above, please do not use the syntax here

With `.moban.yml`, you can copy templates to your destination. Please be
aware that it is not the same as 'cp', 'copy' commands you have experienced.


Please be aware that, your templates and template folder have to be inside
declared template folders. It does not copy any file or folder.


Here is example moban file for copying::
  
    configuration:
      template_dir:
        - template-sources
    copy:
      - simple.file.copy: file-in-template-sources-folder.txt
      - "misc-1-copying/can-create-folder/if-not-exists.txt": file-in-template-sources-folder.txt
      - "test-dir": dir-for-copying
      - "test-recursive-dir": dir-for-recusive-copying/**


template copy does:


#. copies any template inside pre-declared template directory to anywhere. moban will create directory if needed.
#. copies any directory to anywhere. If "**" is followed, moban attempts to do recursive copying.
