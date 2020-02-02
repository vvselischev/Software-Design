from bash.interpreter.channels.output_channel import OutputChannel


class StdoutChannel(OutputChannel):
    """Wraps the stdout channel. Does not print the new line at the end."""
    def write(self, value):
        print(value, end='')
