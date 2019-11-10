Level 23: moban file inheritance
================================================================================

It is a bit tedious to repeat a few common configuration in moban file. Why not
create a parent moban file? Then allow child project to deviate from.

The answer is to use 'overrides' in `.moban.yaml`, so called moban file.

`overrides` could over ride any data file format in any location in theory. And
it support override a specific key set.
