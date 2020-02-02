from ..command import Command


class Wc(Command):
    """
    Prints an information of a given file or of the stdin in a format:
    [lines] [words] [bytes]
    The first argument must be 'wc'. The second argument is an optional name of a file.
    Executed with one argument, reads a content from the stdin.
    Appends the result with a new line.
    """
    def execute(self):
        if len(self._args) > 2:
            raise Exception("Too many arguments for wc. Found: " +
                            str(len(self._args)))

        if len(self._args) == 2:
            with open(self._args[1], 'r') as file:
                input_content = file.read()
        elif self._input_channel:
            input_content = self._input_channel.read()
        else:
            raise Exception("Not enough arguments for command 'wc'.")

        self.__process_content(input_content)

    def __process_content(self, content):
        lines = len(content.splitlines())
        words = len(content.split())
        bytes_number = len(content.encode('utf-8'))
        self._output_channel.write(str(lines) + " ")
        self._output_channel.write(str(words) + " ")
        self._output_channel.write(str(bytes_number) + '\n')
