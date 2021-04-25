import abc


class InputChannel(abc.ABC):
    """Represents an abstract channel to read from."""
    @abc.abstractmethod
    def read(self):
        raise NotImplementedError('Implement in subclass')
