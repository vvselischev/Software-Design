from ..command import Command


class Exit(Command):
    """
    Stops the given controller.
    Must be called with a single argument 'exit'.
    """
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def execute(self):
        if len(self._args) != 1:
            raise Exception("Invalid argument number in exit. Found: " +
                            str(len(self._args)))

        self.controller.stop()
