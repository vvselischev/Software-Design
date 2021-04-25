import abc


class ExecutableFactory(abc.ABC):
    """Base class for executable factories."""
    @abc.abstractmethod
    def create_executable(self, tokenized):
        """Returns an executable object created by the given tokenized string."""
        raise NotImplementedError('Implement in subclass')
