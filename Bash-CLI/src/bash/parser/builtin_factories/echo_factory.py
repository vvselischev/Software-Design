from bash.interpreter.builtins.echo import Echo
from .executable_factory import ExecutableFactory


class EchoFactory(ExecutableFactory):
    """
    Creates an echo command by the tokenized string.
    Checks the arguments and passes them in an appropriate format.
    """
    def create_executable(self, tokenized):
        normalized = [token.get_string_with_normalized_quotes() for token in tokenized.to_list()]
        self.__check_args(normalized)

        command = Echo()
        command.set_args(normalized)
        return command

    def __check_args(self, args):
        if not (len(args) > 0 and args[0] == "echo"):
            raise Exception("Invalid command format: echo.")
