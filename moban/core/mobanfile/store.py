class Store:
    def __init__(self):
        self.init()

    def add(self, target):
        self.targets.append(target)
        self.look_up_by_output[target.output] = target

    def init(self):
        self.targets = []
        self.look_up_by_output = {}
        self.intermediate_targets = []


STORE = Store()
