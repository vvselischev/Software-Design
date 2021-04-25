import os


class Environment:
    """Represents an environment with a dict interface."""
    def __init__(self):
        self._variables = {}

    def put(self, variable, value):
        """Puts the pair to the environment or updates the existing variable."""
        self._variables[variable] = value

    def get(self, name):
        """
        Returns a value of a given variable or
        throws an exception if it does not exist.
        """
        if name not in self._variables:
            raise Exception("Variable " + name + " is not in the environment.")
        return self._variables[name]

    def update_system_environment(self):
        """Copies all variables to the system environment."""
        for key, value in self._variables:
            os.environ[key] = value
