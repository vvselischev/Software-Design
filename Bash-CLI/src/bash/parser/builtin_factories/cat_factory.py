from bash.interpreter.builtins.cat import Cat
from .executable_factory import ExecutableFactory


class CatFactory(ExecutableFactory):
    """
    Creates a cat command by the tokenized string.
    Checks the arguments and passes them in an appropriate format.
    """
    def create_executable(self, tokenized):
        normalized = [token.get_string_with_normalized_quotes() for token in tokenized.to_list()]
        self.__check_args(normalized)

        command = Cat()
        command.set_args(normalized)
        return command

    def __check_args(self, args):
        if not (len(args) > 0 and args[0] == "cat"):
            raise Exception("Invalid command format: cat.")
