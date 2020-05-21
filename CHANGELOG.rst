Change log
================================================================================

0.7.5 - 21.5.2020
--------------------------------------------------------------------------------

**Added**

#. `#167 <https://github.com/moremoban/moban/issues/167>`_: reverse what moban
   have done: delete

0.7.4 - 13.5.2020
--------------------------------------------------------------------------------

**Fixed**

#. `#378 <https://github.com/moremoban/moban/issues/378>`_: suppress stdout
   message from deprecated pip install. but please do not use and migrate
   deprecated`requires` syntax.

0.7.3 - 2.5.2020
--------------------------------------------------------------------------------

**Added**

#. Added continuous check in travis for setup.py descriptions. No impact to
   moban user.

0.7.2 - 1.5.2020
--------------------------------------------------------------------------------

**Added**

#. Support for templates and configuration files over HTTP(S) protocol with
   httpfs! Yepee!

0.7.1 - 25.04.2020
--------------------------------------------------------------------------------

**Fixed**

#. `#365 <https://github.com/moremoban/moban/issues/365>`_: regression was
   introduced by v0.6.5. If you uses mobanfile as data configuration file, you
   are very likely to have this show stopper. Please upgrade to this version.

0.7.0 - 18.01.2020
--------------------------------------------------------------------------------

**Removed**

#. `#360 <https://github.com/moremoban/moban/issues/360>`_: make gitfs2 and
   pypifs optional.
#. `#303 <https://github.com/moremoban/moban/issues/303>`_: python 2.7 support
   is dropped.

**Updated**

#. `#360 <https://github.com/moremoban/moban/issues/360>`_: show friendlier
   error when unknown protocol exception was raised.

0.6.8 - 7.12.2019
--------------------------------------------------------------------------------

**Updated**

#. since version 0.5.0, when rendering a single file or string, moban would
   report 'Templated 1 of 0 files', which should have been 'Templated 1 file.' 

**Removed**

#. python 3.4 support is gone because colorama requires Python '>=2.7, !=3.0.*,
   !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*' 

0.6.7 - 1.12.2019
--------------------------------------------------------------------------------

**Updated**

#. no verbose for error, -v for warning, -vv for warning+info, -vvv for
   warning+info+debug
#. `#351 <https://github.com/moremoban/moban/issues/351>`_, show template plugin
   name, i.e. 'copying' for copy instead of 'templating'

**Removed**

#. Message: 'Warning: Attempting to use environment vars as data...' became
   warning log
#. Message: 'Warning: Both data.yml and /.../.moban.cd/data.yml does not exist'
   became warning log
#. with -v, you would see them in such a situation

0.6.6 - 10.11.2019
--------------------------------------------------------------------------------

**Added**

#. support moban file inheritance. one base moban file and child repos can
   inherit and override

0.6.5 - 13.10.2019
--------------------------------------------------------------------------------

**Added**

#. `#335 <https://github.com/moremoban/moban/issues/335>`_: support intermediate
   targets in moban file

0.6.4 - 4.10.2019
--------------------------------------------------------------------------------

**Updated**

#. Command options have been grouped. --template_type became --template-type
#. Increment gitfs2 to version 0.0.2. `gitfs#4
   <https://github.com/moremoban/gitfs/issues/4>`_

0.6.3 - 25.09.2019
--------------------------------------------------------------------------------

**Added**

#. `#260 <https://github.com/moremoban/moban/issues/260>`_: jinja-cli parity:
   support command line pipe stream.

0.6.2 - 15.09.2019
--------------------------------------------------------------------------------

**Added**

#. `#322 <https://github.com/moremoban/moban/issues/322>`_: Implicit targets
   with template extensions default to copy
#. `#257 <https://github.com/moremoban/moban/issues/257>`_: '-e' to load
   extensions for template engines, i.e. jinja2
#. `#333 <https://github.com/moremoban/moban/issues/333>`_: command line
   template fails with version 0.6.1

0.6.1 - 10.09.2019
--------------------------------------------------------------------------------

**Fixed**

#. `#328 <https://github.com/moremoban/moban/issues/328>`_: update backward
   compatibility

0.6.0 - 10.09.2019
--------------------------------------------------------------------------------

**Added**

#. `#205 <https://github.com/moremoban/moban/issues/205>`_: support
   `pyFilesystem2 <https://pyfilesystem2.readthedocs.io/>`_
#. `#185 <https://github.com/moremoban/moban/issues/185>`_: -v will enable moban
   application logging for development. And -V is for version.
#. `#325 <https://github.com/moremoban/moban/issues/325>`_: -vv show debug trace
#. `#126 <https://github.com/moremoban/moban/issues/126>`_: Allow mobanfile to
   include data from arbitrary config files
#. `#256 <https://github.com/moremoban/moban/issues/256>`_: jinja2-cli parity:
   '-d hello=world' to define custom variable on cli

**Updated**

#. `#275 <https://github.com/moremoban/moban/issues/275>`_: fix moban 0.4.5 test
   failures on openSUSE Tumbleweed

0.5.0 - 14.07.2019
--------------------------------------------------------------------------------

**Updated**

#. `#277 <https://github.com/moremoban/moban/issues/277>`_: Restored dependency
   git-url-parse, replacing incompatible giturlparse which was used during moban
   0.4.x
#. `#281 <https://github.com/moremoban/moban/issues/281>`_: Fixed unicode
   support on Python 2.7
#. `#274 <https://github.com/moremoban/moban/issues/274>`_: Updated ruamel.yaml
   dependency pins to restore support for Python 3.4, and prevent installation
   of versions that can not be installed on Python 3.7
#. `#285 <https://github.com/moremoban/moban/issues/285>`_: Fixed CI testing of
   minimum requirements
#. `#271 <https://github.com/moremoban/moban/issues/271>`_: Fixed repository
   caching bug preventing branch switching
#. `#292 <https://github.com/moremoban/moban/issues/292>`_: Reformatted YAML
   files according to yamllint rules
#. `#291 <https://github.com/moremoban/moban/issues/291>`_: Fixed filename typos
   in README
#. `#280 <https://github.com/moremoban/moban/issues/280>`_: Added CI to ensure
   repository is in sync with upstream
#. `#280 <https://github.com/moremoban/moban/issues/280>`_: sync setup.py from
   pypi-mobans

0.4.5 - 07.07.2019
--------------------------------------------------------------------------------

**Updated**

#. `#271 <https://github.com/moremoban/moban/issues/271>`_: support git branch
   change in later run.

0.4.4 - 26.05.2019
--------------------------------------------------------------------------------

**Updated**

#. `#265 <https://github.com/moremoban/moban/issues/265>`_: Use simple `read
   binary` to read instead of encoding

0.4.3 - 16.03.2019
--------------------------------------------------------------------------------

**Removed**

#. `#253 <https://github.com/moremoban/moban/issues/253>`_: symbolic link in
   regression pack causes python setup.py to do recursive include

**Added**

#. `#209 <https://github.com/moremoban/moban/issues/209>`_: Alert moban user
   when `git` is not available and is used.

**Updated**

#. `#261 <https://github.com/moremoban/moban/issues/261>`_: since moban group
   template files per template type, this fill use first come first register to
   order moban group

0.4.2 - 08.03.2019
--------------------------------------------------------------------------------

**Added**

#. `#234 <https://github.com/moremoban/moban/issues/234>`_: Define template
   parameters on the fly inside `targets` section
#. `#62 <https://github.com/moremoban/moban/issues/62>`_: select a group target
   to run

**Updated**

#. `#180 <https://github.com/moremoban/moban/issues/180>`_: No longer two
   statistics will be shown in v0.4.x. legacy copy targets are injected into a
   normal targets. cli target is made a clear priority.
#. `#244 <https://github.com/moremoban/moban/issues/244>`_: version 0.4.2 is
   first version which would work perfectly on windows since 17 Nov 2018. Note
   that: file permissions are not used on windows. Why the date? because
   samefile is not avaiable on windows, causing unit tests to fail hence it lead
   to my conclusion that moban version between 17 Nov 2018 and March 2019 wont
   work well on Windows.

0.4.1 - 28.02.2019
--------------------------------------------------------------------------------

**Added**

#. `#235 <https://github.com/moremoban/moban/issues/235>`_: user defined
   template types so that custom file extensions, template configurations can be
   controlled by moban user
#. `#232 <https://github.com/moremoban/moban/issues/232>`_: the package
   dependencies have been fine tuning to lower versions, most of them are dated
   back to 2017.

0.4.0 - 20.02.2019
--------------------------------------------------------------------------------

**Added**

#. `#165 <https://github.com/moremoban/moban/issues/165>`_: Copy as plugins

**Updated**

#. `#219 <https://github.com/moremoban/moban/issues/219>`_: git clone depth set
   to 2
#. `#186 <https://github.com/moremoban/moban/issues/186>`_: lowest dependecy on
   ruamel.yaml is 0.15.5, Jun 2017

0.3.10 - 03.02.2019
--------------------------------------------------------------------------------

**Added**

#. `#174 <https://github.com/moremoban/moban/issues/174>`_: Store git cache in
   XDG_CACHE_DIR
#. `#107 <https://github.com/moremoban/moban/issues/107>`_: Add -v to show
   current moban version
#. `#164 <https://github.com/moremoban/moban/issues/164>`_: support additional
   data formats

**Updated**

#. `#178 <https://github.com/moremoban/moban/issues/178>`_: UnboundLocalError:
   local variable 'target' referenced before assignment
#. `#169 <https://github.com/moremoban/moban/issues/169>`_: uses GitPython
   instead of barebone git commands

0.3.9 - 18-1-2019
--------------------------------------------------------------------------------

**Updated**

#. `#90 <https://github.com/moremoban/moban/issues/90>`_: allow adding extra
   jinja2 extensions. `jinja2.ext.do`, `jinja2.ext.loopcontrols` are included by
   default. what's more, any other template enigne are eligible for extension
   additions.
#. `#158 <https://github.com/moremoban/moban/issues/158>`_: Empty file
   base_engine.py is finally removed

0.3.8 - 12-1-2019
--------------------------------------------------------------------------------

**Updated**

#. `#141 <https://github.com/moremoban/moban/issues/141>`_: disable file
   permissions copy feature and not to check file permission changes on windows.
#. `#154 <https://github.com/moremoban/moban/issues/154>`_: introduce first ever
   positional argument for string base template.
#. `#157 <https://github.com/moremoban/moban/issues/157>`_: the exit code
   behavior changed. for backward compactibility please use --exit-code.
   Otherwise, moban will not tell if there is any changes.

0.3.7 - 6-1-2019
--------------------------------------------------------------------------------

**Updated**

#. `#146 <https://github.com/moremoban/moban/issues/146>`_: added a low-setup
   usage mode via environment variables to moban
#. `#148 <https://github.com/moremoban/moban/issues/148>`_: include test related
   files in the package for package validation when distributing via linux
   system, i.e. OpenSuse

0.3.6 - 30-12-2018
--------------------------------------------------------------------------------

**Updated**

#. `#143 <https://github.com/moremoban/moban/issues/143>`_: moban shall report
   permission error and continue the rest of the copying task.
#. `#122 <https://github.com/moremoban/moban/issues/122>`_: Since 0.3.6, moban
   is tested on windows and macos too, using azure build pipelines. It is
   already tested extensively on travis-ci on linux os.

0.3.5 - 10-12-2018
--------------------------------------------------------------------------------

**Updated**

#. `#37 <https://github.com/moremoban/moban/issues/37>`_: moban will report line
   number where the value is empty and the name of mobanfile. Switch from pyyaml
   to ruamel.yaml.

0.3.4.1 - 28-11-2018
--------------------------------------------------------------------------------

**Updated**

#. `#137 <https://github.com/moremoban/moban/issues/137>`_: missing
   contributors.rst file

0.3.4 - 18-11-2018
--------------------------------------------------------------------------------

**Added**

#. global variables to store the target and template file names in the jinja2
   engine
#. moban-handlebars is tested to work well with this version and above

**Updated**

#. Template engine interface has been clarified and documented

0.3.3 - 05-11-2018
--------------------------------------------------------------------------------

**Added**

#. alternative and expanded syntax for requires, so as to accomendate github
   submodule recursive

0.3.2 - 04-11-2018
--------------------------------------------------------------------------------

**Added**

#. configuration dirs may be located by `requires`, i.e. configuration files may
   be in a python package or git repository.

0.3.1 - 02-11-2018
--------------------------------------------------------------------------------

**Added**

#. `#97 <https://github.com/moremoban/moban/issues/97>`_: requires will clone a
   repo if given. Note: only github, gitlab, bitbucket for now

0.3.0 - 27-18-2018
--------------------------------------------------------------------------------

**Added**

#. `#89 <https://github.com/moremoban/moban/issues/89>`_: Install pypi-hosted
   mobans through requires syntax

**Updated**

#. `#96 <https://github.com/moremoban/moban/issues/96>`_: Fix for
   FileNotFoundError for plugins
#. various documentation updates

**Removed**

#. `#88 <https://github.com/moremoban/moban/issues/88>`_: removed python 2.6
   support
#. removed python 3.3 support

0.2.4 - 14-07-2018
--------------------------------------------------------------------------------

**Added**

#. `#32 <https://github.com/moremoban/moban/issues/32>`_: option 1 copy a
   directory without its subdirectories.
#. `#30 <https://github.com/moremoban/moban/issues/30>`_: command line template
   option is ignore when a moban file is present

0.2.3 - 10-07-2018
--------------------------------------------------------------------------------

**Added**

#. `#76 <https://github.com/moremoban/moban/issues/76>`_: running moban as a
   module from python command
#. `#32 <https://github.com/moremoban/moban/issues/32>`_: copy a directory
   recusively
#. `#33 <https://github.com/moremoban/moban/issues/33>`_: template all files in
   a directory

0.2.2 - 16-06-2018
--------------------------------------------------------------------------------

**Added**

#. `#31 <https://github.com/moremoban/moban/issues/31>`_: create directory if
   missing during copying

**Updated**

#. `#28 <https://github.com/moremoban/moban/issues/28>`_: if a template has been
   copied once before, it is skipped in the next moban call

0.2.1 - 13-06-2018
--------------------------------------------------------------------------------

**Updated**

#. templates using the same template engine will be templated as a group
#. update lml dependency to 0.0.3

0.2.0 - 11-06-2018
--------------------------------------------------------------------------------

**Added**

#. `#18 <https://github.com/moremoban/moban/issues/18>`_: file exists test
#. `#23 <https://github.com/moremoban/moban/issues/23>`_: custom jinja plugins
#. `#26 <https://github.com/moremoban/moban/issues/26>`_: repr filter
#. `#47 <https://github.com/moremoban/moban/issues/47>`_: allow the expansion of
   template engine
#. `#58 <https://github.com/moremoban/moban/issues/58>`_: allow template type
   per template

**Updated**

#. `#34 <https://github.com/moremoban/moban/issues/34>`_: fix plural message if
   single file is processed

0.1.4 - 29-May-2018
--------------------------------------------------------------------------------

**Updated**

#. `#21 <https://github.com/moremoban/moban/issues/21>`_: targets become
   optional
#. `#19 <https://github.com/moremoban/moban/issues/19>`_: transfer symlink's
   target file's file permission under unix/linux systems
#. `#16 <https://github.com/moremoban/moban/issues/16>`_: introduce copy key
   word in mobanfile

0.1.3 - 12-Mar-2018
--------------------------------------------------------------------------------

**Updated**

#. handle unicode on python 2

0.1.2 - 10-Jan-2018
--------------------------------------------------------------------------------

**Added**

#. `#13 <https://github.com/moremoban/moban/issues/13>`_: strip off new lines in
   the templated file

0.1.1 - 08-Jan-2018
--------------------------------------------------------------------------------

**Added**

#. the ability to present a long text as multi-line paragraph with a custom
   upper limit
#. speical filter expand github references: pull request and issues
#. `#15 <https://github.com/moremoban/moban/issues/15>`_: fix templating syntax
   to enable python 2.6

0.1.0 - 19-Dec-2017
--------------------------------------------------------------------------------

**Added**

#. `#14 <https://github.com/moremoban/moban/issues/14>`_, provide shell exit
   code

0.0.9 - 24-Nov-2017
--------------------------------------------------------------------------------

**Added**

#. `#11 <https://github.com/moremoban/moban/issues/11>`_, recognize .moban.yaml
   as well as .moban.yml.
#. `#9 <https://github.com/moremoban/moban/issues/9>`_, preserve file
   permissions of the source template.
#. `-m` option is added to allow you to specify a custom moban file. kinda
   related to issue 11.

**Updated**

#. use explicit version name: `moban_file_spec_version` so that `version` can be
   used by users. `#10 <https://github.com/moremoban/moban/issues/10>`_ Please
   note: moban_file_spec_version is reserved for future file spec upgrade. For
   now, all files are assumed to be '1.0'. When there comes a new version i.e.
   2.0, new moban file based on 2.0 will have to include
   'moban_file_spec_version: 2.0'

0.0.8 - 18-Nov-2017
--------------------------------------------------------------------------------

**Added**

#. `#8 <https://github.com/moremoban/moban/issues/8>`_, verify the existence of
   custom template and configuration directories. default .moban.td, .moban.cd
   are ignored if they do not exist.

**Updated**

#. Colorize error messages and processing messages. crayons become a dependency.

0.0.7 - 19-Jul-2017
--------------------------------------------------------------------------------

**Added**

#. Bring the visibility of environment variable into jinja2 templating process:
   `#7 <https://github.com/moremoban/moban/issues/7>`_

0.0.6 - 16-Jun-2017
--------------------------------------------------------------------------------

**Added**

#. added '-f' flag to force moban to template all files despite of .moban.hashes

**Updated**

#. moban will not template target file in the situation where the changes
   occured in target file than in the source: the template file + the data
   configuration after moban has been applied. This new release will remove the
   change during mobanization process.

0.0.5 - 17-Mar-2017
--------------------------------------------------------------------------------

**Added**

#. Create a default hash store when processing a moban file. It will save
   unnecessary file write to the disc if the rendered content is not changed.
#. Added summary reports

0.0.4 - 11-May-2016
--------------------------------------------------------------------------------

**Updated**

#. Bug fix `#5 <https://github.com/moremoban/moban/issues/5>`_, should detect
   duplicated targets in `.moban.yml` file.

0.0.3 - 09-May-2016
--------------------------------------------------------------------------------

**Updated**

#. Bug fix `#4 <https://github.com/moremoban/moban/issues/4>`_, keep trailing
   new lines

0.0.2 - 27-Apr-2016
--------------------------------------------------------------------------------

**Updated**

#. Bug fix `#1 <https://github.com/moremoban/moban/issues/1>`_, failed to save
   utf-8 characters

0.0.1 - 23-Mar-2016
--------------------------------------------------------------------------------

**Added**

#. Initial release
