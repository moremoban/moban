Level 22: intermediate targets
================================================================================

It is natural to allow intermediate target to be source so that different
moban plugins can interact with each other. The good news is since moban verion
0.6.5, it is support.

.. note::
   The bad news is, folder as imtermediate target is not supported yet and will be
   considered in next incremental build. For now, the date cannot be confirmed.

Here are the syntax::
 
   targets:
     - intermediate.jj2: original.jj2
     - final: intermediate.jj2

With moban 0.6.4-, above syntax cannot result in `final` file to be generated
because `intermediate.jj2` does not exist until moban is run.
