import abc


class OutputChannel(abc.ABC):
    """Represents an abstract channel to write to."""
    @abc.abstractmethod
    def write(self, value):
        raise NotImplementedError('Implement in subclass')
