import os
from moban.template import do_template, open_yaml

        
def test_templating():
    base_dir = os.path.join("tests", "fixtures")
    variables = open_yaml(os.path.join(base_dir, "config"),
                          os.path.join(base_dir, "child.yaml"))
    do_template(base_dir, variables, [("a.template", 'test')])
    with open("test", "r") as f:
        content = f.read()
        assert content == "hello world ox"
    os.unlink("test")