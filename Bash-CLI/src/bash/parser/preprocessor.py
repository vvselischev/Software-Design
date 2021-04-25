from bash.parser.token import TokenType, Token
from bash.parser.tokenized import Tokenized


class Preprocessor:
    """Represents an object that substitutes variables in tokenized string."""
    def process(self, tokenized, environment):
        """
        Returns a Tokenized object with substituted variables from the environment
        in the given tokenized string.
        Substitution is not performed inside single quotes.
        An exception is throwing if there is no variable in the environment.
        Substitution is performed only in one pass.
        Token types are not changed after the substitution.
        """
        result = Tokenized()
        for token in tokenized.to_list():
            string_value = token.get_string_value()
            token_type = token.get_token_type()
            if token_type != TokenType.SINGLE_QUOTED:
                string_value = self.__substitute(string_value, environment)
            result.add(Token(token_type, string_value))
        return result

    def __substitute(self, string, environment):
        result = ""
        variable_start_index = -1

        for current_index in range(len(string)):
            if not str.isalnum(string[current_index]):
                if variable_start_index != -1:
                    # We need to skip the dollar in the beginning.
                    variable_name = string[variable_start_index + 1:current_index]
                    variable_value = environment.get(variable_name)
                    result += variable_value
                    variable_start_index = -1

                if string[current_index] == '$':
                    variable_start_index = current_index
                else:
                    result += string[current_index]
            elif variable_start_index == -1:
                result += string[current_index]

        if variable_start_index != -1:
            variable_name = string[variable_start_index + 1:]
            variable_value = environment.get(variable_name)
            result += variable_value

        return result
