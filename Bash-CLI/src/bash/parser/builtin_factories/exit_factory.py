from bash.interpreter.builtins.exit import Exit
from .executable_factory import ExecutableFactory


class ExitFactory(ExecutableFactory):
    """
    Creates an exit command by the tokenized string.
    Checks that no arguments are passed except the command name.
    """
    def __init__(self, controller):
        self.controller = controller

    def create_executable(self, tokenized):
        args = tokenized.to_string_list()
        self.__check_args(args)

        command = Exit(self.controller)
        command.set_args(args)
        return command

    def __check_args(self, args):
        if not args == ["exit"]:
            raise Exception("Invalid command format: exit.")
