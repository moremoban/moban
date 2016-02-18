import os
from moban.template import do_template

        
def test_templating():
    base_dir = os.path.join("tests", "fixtures")
    options = {
        "configuration_dir": os.path.join(base_dir, "config"),
        "template_dir": base_dir
    }
    do_template(options, [
        (os.path.join(base_dir, "child.yaml"),
         "a.template",
         'test')]
    )
    with open("test", "r") as f:
        content = f.read()
        assert content == "hello world ox"
    os.unlink("test")