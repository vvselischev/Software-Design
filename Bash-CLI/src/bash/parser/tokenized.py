class Tokenized:
    """Represents a list of tokens."""
    def __init__(self):
        self._tokens = []

    def add(self, token):
        """Adds a token to the end of the list."""
        self._tokens.append(token)

    def make_string(self):
        """Returns a concatenation of tokens string representations."""
        return "".join([token.get_string_value() for token in self._tokens])

    def contains_token(self, token_type):
        """Checks whether there exist at least one token with a given type."""
        filtered = list(filter(lambda token: token.get_token_type() == token_type, self._tokens))
        return len(filtered) > 0

    def remove(self, token_type):
        """Removes all tokens with the given type from the list."""
        self._tokens = list(filter(lambda token: token.get_token_type() != token_type, self._tokens))

    def first(self):
        """Returns the first token or throws an exception if the list is empty."""
        if not self._tokens:
            raise Exception("An attempt to get first token of the empty Tokenized object.")
        return self._tokens[0]

    def size(self):
        """Returns the number of tokens in the list."""
        return len(self._tokens)

    def to_list(self):
        """Returns a python list of tokens."""
        return list.copy(self._tokens)

    def to_string_list(self):
        """Returns a python list of tokens string representations."""
        return [token.get_string_value() for token in self._tokens]

    @staticmethod
    def from_list(tokens):
        """Creates an object from the given python list of tokens."""
        result = Tokenized()
        for token in tokens:
            result.add(token)
        return result

    def split_by_type(self, token_type):
        """
        Splits the list by the given token type and
        returns a python list of Tokenized objects.
        Tokens of the given type are not included.
        """
        result = [Tokenized()]

        for i, token in enumerate(self._tokens):
            if token.get_token_type() != token_type:
                result[-1].add(token)
            else:
                result.append(Tokenized())
        return result
