from ..command import Command


class Assign(Command):
    """
    Assignment operator. Takes 3 arguments: [variable][=][value].
    Updates the given environment accordingly.
    """
    def __init__(self, environment):
        super().__init__()
        self.environment = environment

    def execute(self):
        if len(self._args) != 3:
            raise Exception("Invalid argument number in assignment. Found: " +
                            str(len(self._args)))

        self.environment.put(self._args[0], self._args[2])
