from bash.interpreter.builtins.call_external import CallExternal
from .executable_factory import ExecutableFactory


class CallExternalFactory(ExecutableFactory):
    """
    Creates an external command by the tokenized string.
    """
    def __init__(self, environment):
        self.environment = environment

    def create_executable(self, tokenized):
        args = tokenized.to_string_list()
        command = CallExternal(self.environment)
        command.set_args(args)
        return command
