Level 21-c: template copying from a tar to a zip
================================================================================

Here is another set of regression tests file for ::

    configuration:
      template_dir:
        - "tar://template-sources.tar"
    targets:
      - output: "zip://my.zip!/simple.file.copy"
        template: file-in-template-sources-folder.txt
        template_type: copy
      - output: "zip://my.zip!/target_without_template_type"
        template: file_extension_will_trigger.copy
      - "zip://my.zip!/target_in_short_form": as_long_as_this_one_has.copy
      - output: "zip://my.zip!/misc-1-copying/can-create-folder/if-not-exists.txt"
        template: file-in-template-sources-folder.txt
        template_type: copy
      - output: "zip://my.zip!/test-dir"
        template: dir-for-copying
        template_type: copy
      - output: "zip://my.zip!/test-recursive-dir"
        template: dir-for-recusive-copying/**
        template_type: copy
