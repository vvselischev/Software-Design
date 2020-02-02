import pytest

from bash.parser import Parser, TokenType
from bash.parser.token import Token


def __check_token(expected, actual):
    assert expected.get_token_type() == actual.get_token_type()
    assert expected.get_string_value() == actual.get_string_value()


def test_parse_empty():
    parser = Parser()
    command = ""
    tokenized = parser.parse(command).to_list()

    assert len(tokenized) == 0


def test_parse_spaces():
    parser = Parser()
    command = "   "
    tokenized = parser.parse(command).to_list()

    assert len(tokenized) == 3
    for token in tokenized:
        __check_token(Token(TokenType.EMPTY, " "), token)


def test_parse_simple():
    parser = Parser()
    command = "simple 123"
    tokenized = parser.parse(command).to_list()

    assert len(tokenized) == 3
    __check_token(Token(TokenType.SIMPLE, "simple"), tokenized[0])
    __check_token(Token(TokenType.EMPTY, " "), tokenized[1])
    __check_token(Token(TokenType.SIMPLE, "123"), tokenized[2])


def test_parse_spaces_at_ends():
    parser = Parser()
    command = " simple "
    tokenized = parser.parse(command).to_list()

    assert len(tokenized) == 3
    __check_token(Token(TokenType.EMPTY, " "), tokenized[0])
    __check_token(Token(TokenType.SIMPLE, "simple"), tokenized[1])
    __check_token(Token(TokenType.EMPTY, " "), tokenized[2])


def test_parse_double_quotes():
    parser = Parser()
    command = "\"double\""
    tokenized = parser.parse(command).to_list()

    assert len(tokenized) == 1
    __check_token(Token(TokenType.DOUBLE_QUOTED, "\"double\""), tokenized[0])


def test_parse_single_quotes():
    parser = Parser()
    command = "'single'"
    tokenized = parser.parse(command).to_list()

    assert len(tokenized) == 1
    __check_token(Token(TokenType.SINGLE_QUOTED, "'single'"), tokenized[0])


def test_parse_single_quotes_inside_double():
    parser = Parser()
    command = "\"'1'\""
    tokenized = parser.parse(command).to_list()

    assert len(tokenized) == 1
    __check_token(Token(TokenType.DOUBLE_QUOTED, "\"'1'\""), tokenized[0])


def test_parse_double_quotes_inside_single():
    parser = Parser()
    command = "'\"1\"'"
    tokenized = parser.parse(command).to_list()

    assert len(tokenized) == 1
    __check_token(Token(TokenType.SINGLE_QUOTED, "'\"1\"'"), tokenized[0])


def test_parse_subsequent_quotes():
    parser = Parser()
    command = "''\"\"''"
    tokenized = parser.parse(command).to_list()

    assert len(tokenized) == 3
    __check_token(Token(TokenType.SINGLE_QUOTED, "''"), tokenized[0])
    __check_token(Token(TokenType.DOUBLE_QUOTED, "\"\""), tokenized[1])
    __check_token(Token(TokenType.SINGLE_QUOTED, "''"), tokenized[2])


def test_fail_on_incorrect_quotes():
    parser = Parser()

    mixed = "'\"'\""
    unclosed_single = "'\"\""
    unclosed_double = "''\""

    with pytest.raises(Exception):
        _ = parser.parse(mixed)

    with pytest.raises(Exception):
        _ = parser.parse(unclosed_single)

    with pytest.raises(Exception):
        _ = parser.parse(unclosed_double)


def test_parse_assignment():
    parser = Parser()
    command = "var=\"1\""
    tokenized = parser.parse(command).to_list()

    assert len(tokenized) == 3
    __check_token(Token(TokenType.SIMPLE, "var"), tokenized[0])
    __check_token(Token(TokenType.ASSIGNMENT, "="), tokenized[1])
    __check_token(Token(TokenType.DOUBLE_QUOTED, "\"1\""), tokenized[2])


def test_empty_pipe():
    parser = Parser()
    command = "||"
    tokenized = parser.parse(command).to_list()

    assert len(tokenized) == 2
    __check_token(Token(TokenType.PIPE, "|"), tokenized[0])
    __check_token(Token(TokenType.PIPE, "|"), tokenized[1])


def test_parse_pipe():
    parser = Parser()
    command = "pwd|pwd |pwd | pwd| pwd"
    tokenized = parser.parse(command).to_list()

    expected = [Token(TokenType.SIMPLE, "pwd"),
                Token(TokenType.PIPE, "|"),
                Token(TokenType.SIMPLE, "pwd"),
                Token(TokenType.EMPTY, " "),
                Token(TokenType.PIPE, "|"),
                Token(TokenType.SIMPLE, "pwd"),
                Token(TokenType.EMPTY, " "),
                Token(TokenType.PIPE, "|"),
                Token(TokenType.EMPTY, " "),
                Token(TokenType.SIMPLE, "pwd"),
                Token(TokenType.PIPE, "|"),
                Token(TokenType.EMPTY, " "),
                Token(TokenType.SIMPLE, "pwd")
                ]

    assert len(tokenized) == len(expected)
    for i, token in enumerate(tokenized):
        __check_token(expected[i], token)
