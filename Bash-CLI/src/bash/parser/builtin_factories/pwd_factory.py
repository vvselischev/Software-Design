from bash.interpreter.builtins.pwd import Pwd
from .executable_factory import ExecutableFactory


class PwdFactory(ExecutableFactory):
    """
    Creates a pwd command by the tokenized string.
    Checks that no arguments are passed except the command name.
    """
    def create_executable(self, tokenized):
        args = tokenized.to_string_list()
        self.__check_args(args)

        command = Pwd()
        command.set_args(args)
        return command

    def __check_args(self, args):
        if not args == ["pwd"]:
            raise Exception("Invalid command format: pwd.")
