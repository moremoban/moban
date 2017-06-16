CHANGE Log
================================================================================

0.0.6 - 16-Jun-2017
--------------------------------------------------------------------------------

Added
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. added '-f' flag to force moban to template all files despite of .moban.hashes

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. moban will not template target file in the situation where the changes
   occured in target file than in the source: the template file + the data
   configuration after moban has been applied. This new release will remove the
   change during mobanization process.

0.0.5 - 17-Mar-2017
--------------------------------------------------------------------------------

Added
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. Create a default hash store when processing a moban file. It will save
   unnecessary file write to the disc if the rendered content is not changed.
#. Added summary reports

0.0.4 - 11-May-2016
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. Bug fix `issue 5 <https://github.com/chfw/moban/issues/5>`_, should detect
   duplicated targets in `.moban.yml` file.

0.0.3 - 09-May-2016
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. Bug fix `issue 4 <https://github.com/chfw/moban/issues/4>`_, keep trailing
   new lines

0.0.2 - 27-Apr-2016
--------------------------------------------------------------------------------

Updated
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#. Bug fix `issue 1 <https://github.com/chfw/moban/issues/1>`_, failed to save
   utf-8 characters


0.0.1 - 23-Mar-2016
--------------------------------------------------------------------------------

Initial release
