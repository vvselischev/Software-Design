from ..command import Command


class Echo(Command):
    """
    A command to print its arguments.
    The first argument must be 'echo'. Others are optional.
    Appends the output with a new line.
    Does not read anything from the input channel.
    """
    def execute(self):
        self._output_channel.write(" ".join(self._args[1:]) + '\n')
