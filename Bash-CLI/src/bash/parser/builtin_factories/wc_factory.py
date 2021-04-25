from bash.interpreter.builtins.wc import Wc
from .executable_factory import ExecutableFactory


class WcFactory(ExecutableFactory):
    """
    Creates a wc command by the tokenized string.
    Checks the arguments and passes them in an appropriate format.
    """
    def create_executable(self, tokenized):
        normalized = [token.get_string_with_normalized_quotes() for token in tokenized.to_list()]
        self.__check_args(normalized)

        command = Wc()
        command.set_args(normalized)
        return command

    def __check_args(self, args):
        if not (len(args) <= 2 and args[0] == "wc" and (len(args) == 1 or args[1])):
            raise Exception("Invalid command format: wc.")
