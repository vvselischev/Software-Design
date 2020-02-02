import abc

from .channels.stdout_channel import StdoutChannel
from .executable import Executable


class Command(Executable, abc.ABC):
    """
    An abstract class for executable commands with arguments and optional
    input and output channels.
    By default, uses the stdout channel and does not use the input channel
    (since all commands are supposed to be complete one-liners).
    """
    @abc.abstractmethod
    def execute(self):
        raise NotImplementedError('Implement in subclass')

    def __init__(self):
        self._input_channel = None
        self._output_channel = StdoutChannel()
        self._args = []

    def set_args(self, args):
        self._args = args

    def get_output_channel(self):
        return self._output_channel

    def get_input_channel(self):
        return self._input_channel

    def set_input_channel(self, channel):
        self._input_channel = channel

    def set_output_channel(self, channel):
        self._output_channel = channel
