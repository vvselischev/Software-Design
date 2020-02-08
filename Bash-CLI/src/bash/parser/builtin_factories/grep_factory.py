import argparse

from .executable_factory import ExecutableFactory
from ...interpreter.builtins.grep import Grep


class GrepFactory(ExecutableFactory):
    """
    Creates a grep command by the tokenized string using the argparse library.
    """

    def __init__(self):
        self.__prepare_parser()

    def create_executable(self, tokenized):
        string_args = tokenized.to_string_list()

        if string_args[0] != "grep":
            raise Exception("Failed to create 'grep' command: the first argument must be 'grep'.")
        string_args = string_args[1:]

        args = vars(self._parser.parse_args(string_args))
        return Grep(pattern=args['pattern'],
                    file=args['file'],
                    ignore_case=args['i'],
                    only_words=args['w'],
                    after_lines=args['A'])

    def __prepare_parser(self):
        self._parser = self._NonExitingParser(prog='grep')
        self._parser.add_argument('-i', help='search ignoring case', action='store_true')
        self._parser.add_argument('-w', help='search for whole words only', action='store_true')
        self._parser.add_argument('-A', type=self.__check_lines_number,
                                  help='display lines after the one containing substring',
                                  default=0)
        self._parser.add_argument('pattern', help='a pattern to search for')
        self._parser.add_argument('file', nargs='?', type=argparse.FileType('r'), help='a file to search in')

    def __check_lines_number(self, line_string):
        line_number = int(line_string)
        if line_number < 0:
            raise argparse.ArgumentTypeError("%s is an invalid positive int value" % line_string)
        return line_number

    class _NonExitingParser(argparse.ArgumentParser):
        """
        ArgumentParser calls system.exit in case of Exception by default.
        We need to catch it in order to continue shell execution.
        """
        def error(self, message):
            raise Exception(f'{self.prog}: error: {message}')
