import enum


class TokenType(enum.Enum):
    """A set of existing token types."""
    SIMPLE = 'SIMPLE'
    DOUBLE_QUOTED = 'DOUBLE_QUOTED'
    SINGLE_QUOTED = 'SINGLE_QUOTED'
    PIPE = 'PIPE'
    ASSIGNMENT = 'ASSIGNMENT'
    EMPTY = 'EMPTY'


class Token:
    """Represents a token with its type and string representation."""
    def __init__(self, token_type, string_value):
        self._token_type = token_type
        self._string_value = string_value

    def get_string_with_normalized_quotes(self):
        result_string = self._string_value
        if self._token_type == TokenType.SINGLE_QUOTED or \
                self._token_type == TokenType.DOUBLE_QUOTED:
            if self.__is_quote(self._string_value[0]):
                result_string = self._string_value[1:]
            if result_string and self.__is_quote(result_string[-1]):
                result_string = result_string[:-1]
        return result_string

    def get_token_type(self):
        return self._token_type

    def get_string_value(self):
        return self._string_value

    def __is_quote(self, char):
        return char == '\'' or char == '"'
