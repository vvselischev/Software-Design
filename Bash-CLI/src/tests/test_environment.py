import pytest

from bash.environment import Environment


def test_put_value():
    environment = Environment()
    environment.put("var", "val")
    assert environment.get("var") == "val"


def test_put_twice():
    environment = Environment()
    environment.put("var", "1")
    environment.put("var", "2")
    assert environment.get("var") == "2"


def test_put_several():
    environment = Environment()
    environment.put("var1", "1")
    environment.put("var2", "2")
    environment.put("var3", "3")
    assert environment.get("var1") == "1"
    assert environment.get("var2") == "2"
    assert environment.get("var3") == "3"


def test_invalid_get():
    environment = Environment()
    with pytest.raises(Exception):
        environment.get("var")
