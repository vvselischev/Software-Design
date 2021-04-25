import re

from ..command import Command


class Grep(Command):
    """
    Searches a given pattern in a given file or in a content from stdin.
    Regular expressions are supported in patterns.
    Prints whole lines where pattern is found.
    """

    def __init__(self, pattern, file=None, ignore_case=False, only_words=False, after_lines=0):
        """
        Creates a grep command with parameters
        :param pattern: a pattern to search, regexps are supported
        :param file: a file to search in, input channel by default
        :param ignore_case: search ignoring case, False by default
        :param only_words: search when only whole words are matched, False by default
        :param after_lines: number of lines to print after each line where match occurred
        """
        super().__init__()
        self._ignore_case = ignore_case
        self._only_words = only_words
        self._after_lines = after_lines
        self._pattern = pattern
        self._file = file

    def execute(self):
        if self._file:
            input_content = self._file.read()
        elif self._input_channel:
            input_content = self._input_channel.read()
        else:
            raise Exception("No input found for grep.")

        flag = 0
        if self._ignore_case:
            flag = re.IGNORECASE

        if self._only_words:
            self._pattern = "\\b" + self._pattern + "\\b"

        output_lines = self.__find_lines(input_content, flag)

        output = ""
        if output_lines:
            output = '\n'.join(output_lines) + '\n'

        self._output_channel.write(output)

    def __find_lines(self, input_content, flag):
        lines_to_show = 0
        output_lines = []
        for line in input_content.split('\n'):
            if re.search(self._pattern, line, flag):
                lines_to_show = self._after_lines
                output_lines.append(line)
            else:
                if lines_to_show > 0:
                    lines_to_show -= 1
                    output_lines.append(line)
        return output_lines
