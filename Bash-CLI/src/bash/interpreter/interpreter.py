from bash.environment import Environment
from bash.parser import Parser, Preprocessor, TokenType
from bash.parser.builtin_factories import *


class Interpreter:
    """
    Interprets a command given in a string representation.
    Creates a local environment once constructed.
    """
    def __init__(self, controller):
        self._parser = Parser()
        self._preprocessor = Preprocessor()
        self._controller = controller
        self._environment = Environment()

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

        factory = self.choose_factory(final_tokenized)
        executable = factory.create_executable(final_tokenized)

        executable.execute()

    def choose_factory(self, tokenized):
        """
        Returns an appropriate factory to create the command
        represented with a given tokenized object.
        Passes the environment if necessary.
        Throws an exception if no tokens are found.
        """
        if tokenized.size() == 0:
            raise Exception("Empty expression found.")

        if tokenized.contains_token(TokenType.PIPE):
            return PipeFactory(self)
        if tokenized.contains_token(TokenType.ASSIGNMENT):
            return AssignFactory(self._environment)

        first_token = tokenized.first()
        if first_token.get_string_value() == "exit":
            return ExitFactory(self._controller)

        if first_token.get_string_value() in COMMAND_FACTORIES:
            return COMMAND_FACTORIES[first_token.get_string_value()]

        return CallExternalFactory(self._environment)
