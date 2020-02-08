from . import PipeFactory, AssignFactory, ExitFactory, CallExternalFactory
from .cat_factory import CatFactory
from .echo_factory import EchoFactory
from .grep_factory import GrepFactory
from .pwd_factory import PwdFactory
from .wc_factory import WcFactory
from .. import TokenType


class FactoryManager:
    __COMMAND_FACTORIES = {"cat": CatFactory(),
                           "echo": EchoFactory(),
                           "pwd": PwdFactory(),
                           "wc": WcFactory(),
                           "grep": GrepFactory()
                           }

    def __init__(self, environment, controller):
        self._environment = environment
        self._controller = controller

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

        if first_token.get_string_value() in self.__COMMAND_FACTORIES:
            return self.__COMMAND_FACTORIES[first_token.get_string_value()]

        return CallExternalFactory(self._environment)