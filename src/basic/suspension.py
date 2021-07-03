class Suspension:
    def __init__(self, func):
        self.func = func

    def force(self):
        if callable(self.func):
            self.func = self.func()
        return self.func
