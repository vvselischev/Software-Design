from bash.interpreter.pipe import Pipe
from .executable_factory import ExecutableFactory
from .. import TokenType


class PipeFactory(ExecutableFactory):
    """
    Creates a pipe of commands by the tokenized string.
    Chooses a factory for each command by asking the given interpreter.
    """
    def __init__(self, factory_manager):
        self._factory_manager = factory_manager

    def create_executable(self, tokenized):
        tokenized_commands = tokenized.split_by_type(TokenType.PIPE)
        pipe = Pipe()

        for tokenized_command in tokenized_commands:
            if tokenized_command.size() == 0 or \
                    tokenized_command.contains_token(TokenType.PIPE):
                raise Exception("Invalid command occurred in pipe.")

            factory = self._factory_manager.choose_factory(tokenized_command)
            executable = factory.create_executable(tokenized_command)
            pipe.append(executable)

        return pipe
