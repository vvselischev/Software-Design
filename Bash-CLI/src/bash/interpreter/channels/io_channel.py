from bash.interpreter.channels.input_channel import InputChannel
from bash.interpreter.channels.output_channel import OutputChannel


class IOChannel(InputChannel, OutputChannel):
    """Represents a channel for reading and writing."""
    def __init__(self):
        self.data = ""

    def write(self, value):
        """Appends the value to the inner buffer."""
        self.data += str(value)

    def read(self):
        """Returns the whole inner content. Does not flush the buffer."""
        return self.data
