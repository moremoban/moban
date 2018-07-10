Level 8: Pass a folder full of templates
================================================================================

We already know that in moban file, you can pass
on a dictionary in targets section, and it apply the template. The assumption
was that the template parameter is a file. Now, what if the parameter is a
directory?

When you pass a directory with full of templates, moban will also assume the
target is a directory and will generate the output there. When saving the
files, it will remove its file suffices automatically.
