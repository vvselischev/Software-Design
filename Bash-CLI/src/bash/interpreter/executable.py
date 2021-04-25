import abc


class Executable(abc.ABC):
    """An interface for objects that can be executed."""
    @abc.abstractmethod
    def execute(self):
        raise NotImplementedError('Implement in subclass')
