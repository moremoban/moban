Trouble shooting guide
==========================

1. Why a file was not templated but copied instead?

   It has been coded so that template engine can choose to pass on the template if it failed to handle. Moban will take over
   and use default 'copy' action.

   In order to find out what went wrong, you can use '-vvv' to enable all logs to assist you.
