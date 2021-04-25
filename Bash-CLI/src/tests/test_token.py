from bash.parser.token import Token, TokenType


def test_normalized_single():
    single_quoted = Token(TokenType.SINGLE_QUOTED, "'token'")
    normalized = single_quoted.get_string_with_normalized_quotes()
    assert normalized == "token"


def test_normalized_double():
    single_quoted = Token(TokenType.DOUBLE_QUOTED, "\"token\"")
    normalized = single_quoted.get_string_with_normalized_quotes()
    assert normalized == "token"


def test_not_normalize_simple():
    single_quoted = Token(TokenType.SIMPLE, "\"token\"")
    normalized = single_quoted.get_string_with_normalized_quotes()
    assert normalized == "\"token\""


def test_normalize_only_once_double():
    single_quoted = Token(TokenType.DOUBLE_QUOTED, "\"\"token\"\"")
    normalized = single_quoted.get_string_with_normalized_quotes()
    assert normalized == "\"token\""


def test_normalize_only_once_single():
    single_quoted = Token(TokenType.SINGLE_QUOTED, "\'\'token\'\'")
    normalized = single_quoted.get_string_with_normalized_quotes()
    assert normalized == "\'token\'"
