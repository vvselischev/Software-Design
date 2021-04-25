from bash.environment import Environment
from bash.interpreter.builtins.assign import Assign


def test_assign_number():
    environment = Environment()
    command = Assign(environment)
    command.set_args(["var", "=", "123"])
    command.execute()
    assert environment.get("var") == "123"


def test_assign_special():
    environment = Environment()
    command = Assign(environment)
    command.set_args(["var", "=", "./directory"])
    command.execute()
    assert environment.get("var") == "./directory"


def test_reassign():
    environment = Environment()
    command = Assign(environment)
    command.set_args(["var", "=", "1"])
    command.execute()

    another_command = Assign(environment)
    another_command.set_args(["var", "=", "2"])
    another_command.execute()
    assert environment.get("var") == "2"


def test_assign_different():
    environment = Environment()
    command = Assign(environment)
    command.set_args(["var1", "=", "1"])
    command.execute()

    another_command = Assign(environment)
    another_command.set_args(["var2", "=", "2"])
    another_command.execute()
    assert environment.get("var1") == "1"
    assert environment.get("var2") == "2"
