from bash.interpreter.builtins.assign import Assign
from .executable_factory import ExecutableFactory


class AssignFactory(ExecutableFactory):
    """
    Creates an assignment command by the tokenized string.
    Checks the arguments and passes them in an appropriate format.
    """
    def __init__(self, environment):
        self.environment = environment

    def create_executable(self, tokenized):
        normalized = [token.get_string_with_normalized_quotes() for token in tokenized.to_list()]
        self.__check_args(normalized)

        command = Assign(self.environment)
        command.set_args(normalized)
        return command

    def __check_args(self, args):
        if not (len(args) == 3 and
                args[1] == '=' and
                args[0] and
                args[2] and
                str.isalnum(args[0])):
            raise Exception("Invalid assignment format.")
