from .executable import Executable
from bash.interpreter.channels.io_channel import IOChannel


class Pipe(Executable):
    """Represents a sequence of commands connected with channels."""
    def __init__(self):
        self._commands = []

    def append(self, command):
        """
        Appends a command to the end of the pipe.
        Connects it with a previous one (if exists) with a new channel.
        """
        if self._commands:
            channel_from_last = IOChannel()
            command.set_input_channel(channel_from_last)
            self._commands[-1].set_output_channel(channel_from_last)

        self._commands.append(command)

    def execute(self):
        for command in self._commands:
            command.execute()
