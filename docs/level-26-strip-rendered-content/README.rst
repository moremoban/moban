Level 26: Strip the white spaces
================================================================================

It was requested, a long time ago, to be able to strip the white spaces
before and after the rendered content. Due to these factors:

1. templating order needs to be respected first
2. intermediate targets(moban generated files) can be allowed as template
3. and delete the intermediate file

Now, all three factors are now supported. Hence, 'strip' feature can be
rolled out.

Here is the short syntax::

   targets:
     - final: intermediate_file.strip

Here are the full syntax::

   targets:
     - output: final
       template: intermediate_file.what_ever
       template_type: strip


Example mobanfile::

   targets:
     - intermediate.strip: content_with_lots_of_white_spaces.jj2
     - final: intermediate.strip
     - delete!: intermediate.strip
 
