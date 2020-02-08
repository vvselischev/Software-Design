from bash.environment import Environment
from bash.parser import Parser, Preprocessor, TokenType
from bash.parser.builtin_factories.factory_manager import FactoryManager


class Interpreter:
    """
    Interprets a command given in a string representation.
    Creates a local environment once constructed.
    """
    def __init__(self, controller):
        self._parser = Parser()
        self._preprocessor = Preprocessor()
        self._environment = Environment()
        self._factory_manager = FactoryManager(self._environment, controller)

    def process(self, command):
        """
        Passes the given command through parser and preprocessor.
        Creates and executes a command built with a tokenized result.
        :param command: command in a string representation
        """
        tokenized = self._parser.parse(command)

        substituted = self._preprocessor.process(tokenized, self._environment)

        final_tokenized = self._parser.parse(substituted.make_string())
        # We needed to store empty tokens at the first step to convert the tokenized result
        # to a string to perform substitution.
        final_tokenized.remove(TokenType.EMPTY)

        factory = self._factory_manager.choose_factory(final_tokenized)
        executable = factory.create_executable(final_tokenized)

        executable.execute()
