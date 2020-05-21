Level 25: delete intermediate targets
================================================================================

Continue with level 22, we would like to delete intermediate files.

.. note::

   What is intermediate targets? Simply they are the files moban generates
   but in the end those files are not really used.


For safety reasons, we only delete intermediate targets. We are not allowing
moban to delete any files in template folders and staic folder.

Here is the short syntax::

   targets:
     - delete!: intermediate_file.jj2

Here are the full syntax::

   targets:
     - output: what_ever_here_will_be_ignored
       template: intermediate.jj2
       template_type: delete       
     - output: ''
       template: intermediate2.jj2


Example mobanfile::

   targets:
     - intermediate.jj2: original.jj2
     - intermediate2.jj2: original.jj2
     - intermediate3.jj2: original.jj2
     - output: x
       template: intermediate.jj2
       template_type: delete       
     - output: ''
       template: intermediate2.jj2
     - delete!: intermediate3.jj2
 
