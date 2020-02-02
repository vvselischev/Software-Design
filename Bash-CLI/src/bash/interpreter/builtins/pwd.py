from ..command import Command
from pathlib import Path


class Pwd(Command):
    """
    Prints the current directory where the process is executed.
    Must be called with a single argument 'pwd'.
    """
    def execute(self):
        if len(self._args) != 1:
            raise Exception("Invalid argument number in cat. Found: " +
                            str(len(self._args)))

        self._output_channel.write(str(Path.cwd()) + '\n')
