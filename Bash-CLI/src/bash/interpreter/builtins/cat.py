from ..command import Command


class Cat(Command):
    """
    A command that displays a content of a given file or of the stdin.
    The first argument must be 'cat'. The second argument is an optional name of a file.
    Executed with one argument, reads a content from the stdin.
    Does not append a content with a new line.
    """
    def execute(self):
        if len(self._args) >= 2:
            for path in self._args[1:]:
                with open(path, 'r') as file:
                    content = file.read()
                    self._output_channel.write(content)
        elif self._input_channel:
            input_content = self._input_channel.read()
            self._output_channel.write(input_content)
        else:
            raise Exception("Not enough arguments for command 'cat'.")
