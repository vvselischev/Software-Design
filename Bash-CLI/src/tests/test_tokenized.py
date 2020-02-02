import pytest

from bash.parser.token import Token, TokenType
from bash.parser.tokenized import Tokenized


def test_contains():
    tokenized = Tokenized()
    tokenized.add(Token(TokenType.SIMPLE, "simple"))
    tokenized.add(Token(TokenType.DOUBLE_QUOTED, "\"double\""))
    tokenized.add(Token(TokenType.SINGLE_QUOTED, "'single'"))
    tokenized.add(Token(TokenType.PIPE, "|"))
    tokenized.add(Token(TokenType.ASSIGNMENT, "="))
    tokenized.add(Token(TokenType.EMPTY, " "))

    assert tokenized.contains_token(TokenType.SIMPLE)
    assert tokenized.contains_token(TokenType.DOUBLE_QUOTED)
    assert tokenized.contains_token(TokenType.SINGLE_QUOTED)
    assert tokenized.contains_token(TokenType.PIPE)
    assert tokenized.contains_token(TokenType.ASSIGNMENT)
    assert tokenized.contains_token(TokenType.EMPTY)


def test_not_contains():
    tokenized = Tokenized()

    assert not tokenized.contains_token(TokenType.SIMPLE)
    tokenized.add(Token(TokenType.SIMPLE, "simple"))

    assert not tokenized.contains_token(TokenType.DOUBLE_QUOTED)
    tokenized.add(Token(TokenType.DOUBLE_QUOTED, "\"double\""))

    assert not tokenized.contains_token(TokenType.SINGLE_QUOTED)
    tokenized.add(Token(TokenType.SINGLE_QUOTED, "'single'"))

    assert not tokenized.contains_token(TokenType.PIPE)
    tokenized.add(Token(TokenType.PIPE, "|"))

    assert not tokenized.contains_token(TokenType.ASSIGNMENT)
    tokenized.add(Token(TokenType.ASSIGNMENT, "="))

    assert not tokenized.contains_token(TokenType.EMPTY)


def test_make_string():
    tokenized = Tokenized()
    tokenized.add(Token(TokenType.SIMPLE, "simple"))
    tokenized.add(Token(TokenType.DOUBLE_QUOTED, "\"double\""))
    tokenized.add(Token(TokenType.SINGLE_QUOTED, "'single'"))
    tokenized.add(Token(TokenType.PIPE, "|"))
    tokenized.add(Token(TokenType.ASSIGNMENT, "="))
    tokenized.add(Token(TokenType.EMPTY, " "))

    expected = "simple\"double\"'single'|= "
    assert expected == tokenized.make_string()


def test_to_string_list():
    tokenized = Tokenized()
    tokenized.add(Token(TokenType.SIMPLE, "simple"))
    tokenized.add(Token(TokenType.DOUBLE_QUOTED, "\"double\""))
    tokenized.add(Token(TokenType.SINGLE_QUOTED, "'single'"))
    tokenized.add(Token(TokenType.PIPE, "|"))
    tokenized.add(Token(TokenType.ASSIGNMENT, "="))
    tokenized.add(Token(TokenType.EMPTY, " "))

    expected = ["simple", "\"double\"", "'single'", "|", "=", " "]
    assert expected == tokenized.to_string_list()


def test_remove():
    tokenized = Tokenized()

    tokenized.add(Token(TokenType.SIMPLE, "simple"))
    tokenized.add(Token(TokenType.DOUBLE_QUOTED, "\"double\""))
    tokenized.add(Token(TokenType.SINGLE_QUOTED, "'single'"))
    tokenized.add(Token(TokenType.PIPE, "|"))
    tokenized.add(Token(TokenType.ASSIGNMENT, "="))
    tokenized.add(Token(TokenType.EMPTY, " "))

    tokenized.remove(TokenType.SIMPLE)
    assert not tokenized.contains_token(TokenType.SIMPLE)

    tokenized.remove(TokenType.DOUBLE_QUOTED)
    assert not tokenized.contains_token(TokenType.DOUBLE_QUOTED)

    tokenized.remove(TokenType.SINGLE_QUOTED)
    assert not tokenized.contains_token(TokenType.SINGLE_QUOTED)

    tokenized.remove(TokenType.PIPE)
    assert not tokenized.contains_token(TokenType.PIPE)

    tokenized.remove(TokenType.ASSIGNMENT)
    assert not tokenized.contains_token(TokenType.ASSIGNMENT)

    tokenized.remove(TokenType.EMPTY)
    assert not tokenized.contains_token(TokenType.EMPTY)


def test_first():
    tokenized = Tokenized()

    tokenized.add(Token(TokenType.SIMPLE, "simple"))
    first = tokenized.first()
    assert first.get_token_type() == TokenType.SIMPLE
    assert first.get_string_value() == "simple"

    tokenized.add(Token(TokenType.DOUBLE_QUOTED, "\"double\""))
    assert first.get_token_type() == TokenType.SIMPLE
    assert first.get_string_value() == "simple"


def test_first_of_empty():
    tokenized = Tokenized()

    with pytest.raises(Exception):
        tokenized.first()


def test_size():
    tokenized = Tokenized()

    assert tokenized.size() == 0

    tokenized.add(Token(TokenType.SIMPLE, "simple"))
    assert tokenized.size() == 1

    tokenized.add(Token(TokenType.DOUBLE_QUOTED, "\"double\""))
    assert tokenized.size() == 2


def test_to_list_empty():
    tokenized = Tokenized()
    assert tokenized.to_list() == []


def test_to_list():
    tokenized = Tokenized()
    tokenized.add(Token(TokenType.PIPE, "|"))
    tokenized.add(Token(TokenType.ASSIGNMENT, "="))

    token_list = tokenized.to_list()
    assert token_list[0].get_token_type() == TokenType.PIPE
    assert token_list[0].get_string_value() == "|"
    assert token_list[1].get_token_type() == TokenType.ASSIGNMENT
    assert token_list[1].get_string_value() == "="

    assert len(token_list) == 2


def test_split_by_type_empty():
    tokenized = Tokenized()
    splitted = tokenized.split_by_type(TokenType.SIMPLE)
    assert len(splitted) == 1
    assert splitted[0].size() == 0


def test_split_by_type_with_no_such_type():
    tokenized = Tokenized()
    tokenized.add(Token(TokenType.SIMPLE, "1"))
    tokenized.add(Token(TokenType.ASSIGNMENT, "="))
    splitted = tokenized.split_by_type(TokenType.PIPE)
    assert len(splitted) == 1
    assert splitted[0].to_string_list() == ["1", "="]


def test_split_by_type():
    tokenized = Tokenized()
    tokenized.add(Token(TokenType.SIMPLE, "1"))
    tokenized.add(Token(TokenType.PIPE, "|"))
    tokenized.add(Token(TokenType.PIPE, "|"))
    tokenized.add(Token(TokenType.SIMPLE, "2"))
    tokenized.add(Token(TokenType.SIMPLE, "3"))

    splitted = tokenized.split_by_type(TokenType.PIPE)

    assert len(splitted) == 3
    assert splitted[0].to_string_list() == ["1"]
    assert splitted[1].size() == 0
    assert splitted[2].to_string_list() == ["2", "3"]
