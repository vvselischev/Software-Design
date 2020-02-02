import re

from .token import Token, TokenType
from .tokenized import Tokenized


class Parser:
    """Represents an object that parses strings into tokens."""
    def parse(self, command):
        """Parses the given string into tokens. Returns a Tokenized object."""
        tokens = self.__parse_recursive(command)
        return Tokenized.from_list(tokens)

    def __parse_recursive(self, string):
        if string == "":
            return []

        first_quote = self.__find_first_quote(string)

        if string[first_quote] == '"':
            double_quote, next_double_quote, token = self.__extract_double_quoted(first_quote, string)
            return self.__parse_recursive(string[:double_quote]) + \
                   [token] + \
                   self.__parse_recursive(string[next_double_quote + 1:])

        if string[first_quote] == '\'':
            next_single_quote, single_quote, token = self.__extract_single_quoted(first_quote, string)
            return self.__parse_recursive(string[:single_quote]) + \
                   [token] + \
                   self.__parse_recursive(string[next_single_quote + 1:])

        assignment = string.find('=')
        if assignment != -1:
            token = Token(TokenType.ASSIGNMENT, string[assignment])
            return self.__parse_recursive(string[:assignment]) + \
                   [token] + \
                   self.__parse_recursive(string[assignment + 1:])

        pipe = string.find('|')
        if pipe != -1:
            token = Token(TokenType.PIPE, string[pipe])
            return self.__parse_recursive(string[:pipe]) + \
                   [token] + \
                   self.__parse_recursive(string[pipe + 1:])

        return self.__parse_with_spaces(string)

    def __extract_double_quoted(self, first_quote, string):
        double_quote = first_quote
        next_double_quote = string.find('\"', double_quote + 1)

        if next_double_quote == -1:
            raise Exception("Unclosed double quote.")

        double_quoted_substring = string[double_quote:next_double_quote + 1]
        token = Token(TokenType.DOUBLE_QUOTED, double_quoted_substring)
        return double_quote, next_double_quote, token

    def __extract_single_quoted(self, first_quote, string):
        single_quote = first_quote
        next_single_quote = string.find('\'', single_quote + 1)

        if next_single_quote == -1:
            raise Exception("Unclosed single quote.")

        single_quoted_substring = string[single_quote:next_single_quote + 1]
        token = Token(TokenType.SINGLE_QUOTED, single_quoted_substring)
        return next_single_quote, single_quote, token

    def __find_first_quote(self, string):
        """Returns the position of the first quote in a given string."""
        double_quote = string.find('\"')
        single_quote = string.find('\'')

        if double_quote == -1:
            return single_quote
        if single_quote == -1:
            return double_quote
        return min(double_quote, single_quote)

    def __parse_with_spaces(self, string):
        """Parses tokens separated by spaces into SIMPLE and EMPTY tokens respectively."""
        result = []
        copied = str(string)

        if copied[0] == ' ':
            result.append(Token(TokenType.EMPTY, copied[0]))
            copied = copied[1:]

        ends_with_space = False
        if copied and copied[-1] == ' ':
            ends_with_space = True
            copied = copied[:-1]

        # Using regex to include spaces in the result list
        for word in re.split("( )", copied):
            if len(word) == 0:
                continue
            if word != ' ':
                result.append(Token(TokenType.SIMPLE, word))
            else:
                result.append(Token(TokenType.EMPTY, " "))

        if ends_with_space:
            result.append(Token(TokenType.EMPTY, ' '))

        return result
