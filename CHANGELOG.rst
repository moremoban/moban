Change log
================================================================================

0.1.4 - 29-May-2018
--------------------------------------------------------------------------------

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#21 <https://github.com/moremoban/moban/issues/21>`_: targets become
   optional
#. `#19 <https://github.com/moremoban/moban/issues/19>`_: transfer symlink's
   target file's file permission under unix/linux systems
#. `#16 <https://github.com/moremoban/moban/issues/16>`_: introduce copy key
   word in mobanfile

0.1.3 - 12-Mar-2018
--------------------------------------------------------------------------------

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. handle unicode on python 2

0.1.2 - 10-Jan-2018
--------------------------------------------------------------------------------

Added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#13 <https://github.com/moremoban/moban/issues/13>`_: strip off new lines in
   the templated file

0.1.1 - 08-Jan-2018
--------------------------------------------------------------------------------

Added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. the ability to present a long text as multi-line paragraph with a custom
   upper limit
#. speical filter expand github references: pull request and issues
#. `#15 <https://github.com/moremoban/moban/issues/15>`_: fix templating syntax
   to enable python 2.6

0.1.0 - 19-Dec-2017
--------------------------------------------------------------------------------

Added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#14 <https://github.com/moremoban/moban/issues/14>`_, provide shell exit
   code

0.0.9 - 24-Nov-2017
--------------------------------------------------------------------------------

Added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#11 <https://github.com/moremoban/moban/issues/11>`_, recognize .moban.yaml
   as well as .moban.yml.
#. `#9 <https://github.com/moremoban/moban/issues/9>`_, preserve file
   permissions of the source template.
#. `-m` option is added to allow you to specify a custom moban file. kinda
   related to issue 11.

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. use explicit version name: `moban_file_spec_version` so that `version` can be
   used by users. `#10 <https://github.com/moremoban/moban/issues/10>`_ Please
   note: moban_file_spec_version is reserved for future file spec upgrade. For
   now, all files are assumed to be '1.0'. When there comes a new version i.e.
   2.0, new moban file based on 2.0 will have to include
   'moban_file_spec_version: 2.0'

0.0.8 - 18-Nov-2017
--------------------------------------------------------------------------------

Added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. `#8 <https://github.com/moremoban/moban/issues/8>`_, verify the existence of
   custom template and configuration directories. default .moban.td, .moban.cd
   are ignored if they do not exist.

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Colorize error messages and processing messages. crayons become a dependency.

0.0.7 - 19-Jul-2017
--------------------------------------------------------------------------------

Added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Bring the visibility of environment variable into jinja2 templating process:
   `#7 <https://github.com/moremoban/moban/issues/7>`_

0.0.6 - 16-Jun-2017
--------------------------------------------------------------------------------

Added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. added '-f' flag to force moban to template all files despite of .moban.hashes

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. moban will not template target file in the situation where the changes
   occured in target file than in the source: the template file + the data
   configuration after moban has been applied. This new release will remove the
   change during mobanization process.

0.0.5 - 17-Mar-2017
--------------------------------------------------------------------------------

Added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Create a default hash store when processing a moban file. It will save
   unnecessary file write to the disc if the rendered content is not changed.
#. Added summary reports

0.0.4 - 11-May-2016
--------------------------------------------------------------------------------

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Bug fix `#5 <https://github.com/moremoban/moban/issues/5>`_, should detect
   duplicated targets in `.moban.yml` file.

0.0.3 - 09-May-2016
--------------------------------------------------------------------------------

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Bug fix `#4 <https://github.com/moremoban/moban/issues/4>`_, keep trailing
   new lines

0.0.2 - 27-Apr-2016
--------------------------------------------------------------------------------

Updated
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Bug fix `#1 <https://github.com/moremoban/moban/issues/1>`_, failed to save
   utf-8 characters

0.0.1 - 23-Mar-2016
--------------------------------------------------------------------------------

Added
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Initial release
