import os
from moban.template import do_template


class FakeOptions:
    def __init__(self, **keywords):
        self.__dict__.update(keywords)

        
def test_templating():
    base_dir = os.path.join("tests", "fixtures")
    options = FakeOptions(
        template_dir=base_dir,
        configuration_dir=os.path.join(base_dir, "config"),
        configuration=os.path.join(base_dir, "child.yaml"),
        template="a.template",
        output="test"
    )
    do_template(options)
    with open("test", "r") as f:
        content = f.read()
        assert content == "hello world ox"
    os.unlink("test")