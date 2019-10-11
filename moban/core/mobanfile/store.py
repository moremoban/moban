class Store:
    def __init__(self):
        self.targets = []
        self.look_up_by_output = {}

    def add(self, target):
        self.targets.append(target)
        self.look_up_by_output[target.output] = target


STORE = Store()
