import pytest

from bash.environment import Environment
from bash.parser import Preprocessor
from bash.parser.token import Token, TokenType
from bash.parser.tokenized import Tokenized


def test_single():
    preprocessor = Preprocessor()
    environment = Environment()
    tokenized = Tokenized.from_list([Token(TokenType.SIMPLE, "$var")])
    environment.put("var", "1")

    processed = preprocessor.process(tokenized, environment)

    assert processed.to_string_list() == ["1"]


def test_token_with_no_variable():
    preprocessor = Preprocessor()
    environment = Environment()
    tokenized = Tokenized.from_list([Token(TokenType.SIMPLE, "var")])
    environment.put("var", "1")

    processed = preprocessor.process(tokenized, environment)

    assert processed.to_string_list() == ["var"]


def test_several():
    preprocessor = Preprocessor()
    environment = Environment()
    tokenized = Tokenized.from_list([Token(TokenType.SIMPLE, "$var1"),
                                     Token(TokenType.SIMPLE, "var2"),
                                     Token(TokenType.SIMPLE, "$var3")])
    environment.put("var1", "1")
    environment.put("var2", "2")
    environment.put("var3", "3")

    processed = preprocessor.process(tokenized, environment)

    assert processed.to_string_list() == ["1", "var2", "3"]


def test_single_quoted():
    preprocessor = Preprocessor()
    environment = Environment()
    tokenized = Tokenized.from_list([Token(TokenType.SINGLE_QUOTED, "'$var'")])
    environment.put("var", "1")

    processed = preprocessor.process(tokenized, environment)

    assert processed.to_string_list() == ["'$var'"]


def test_double_quoted():
    preprocessor = Preprocessor()
    environment = Environment()
    tokenized = Tokenized.from_list([Token(TokenType.DOUBLE_QUOTED, "\"var == $var\"")])
    environment.put("var", "1")

    processed = preprocessor.process(tokenized, environment)

    assert processed.to_string_list() == ["\"var == 1\""]


def test_subsequent():
    preprocessor = Preprocessor()
    environment = Environment()
    tokenized = Tokenized.from_list([Token(TokenType.SIMPLE, "$var1$var1")])
    environment.put("var1", "1")

    processed = preprocessor.process(tokenized, environment)

    assert processed.to_string_list() == ["11"]


def test_substitute_only_once():
    preprocessor = Preprocessor()
    environment = Environment()
    tokenized = Tokenized.from_list([Token(TokenType.SIMPLE, "$var1")])
    environment.put("var1", "$var1")

    processed = preprocessor.process(tokenized, environment)

    assert processed.to_string_list() == ["$var1"]


def test_no_variable():
    preprocessor = Preprocessor()
    environment = Environment()
    tokenized = Tokenized.from_list([Token(TokenType.DOUBLE_QUOTED, "var == $var")])

    with pytest.raises(Exception):
        _ = preprocessor.process(tokenized, environment)
