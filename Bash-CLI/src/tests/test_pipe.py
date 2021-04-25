import os

from bash.interpreter.builtins.call_external import CallExternal
from bash.interpreter.builtins.cat import Cat
from bash.interpreter.builtins.echo import Echo
from bash.interpreter.builtins.pwd import Pwd
from bash.interpreter.builtins.wc import Wc
from bash.interpreter.channels.io_channel import IOChannel
from bash.interpreter.pipe import Pipe


def test_pipe_single_command():
    pipe = Pipe()
    command = Echo()
    command.set_args(["echo", "1"])
    output = IOChannel()
    command.set_output_channel(output)
    pipe.append(command)

    pipe.execute()
    assert output.read() == "1\n"


def test_echo_pass_arguments():
    pipe = Pipe()
    first_command = Echo()
    first_command.set_args(["echo", "123"])
    pipe.append(first_command)

    second_command = Cat()
    second_command.set_args(["cat"])
    output = IOChannel()
    second_command.set_output_channel(output)
    pipe.append(second_command)

    pipe.execute()
    assert output.read() == "123\n"


def test_echo_not_read_arguments():
    pipe = Pipe()
    first_command = Cat()
    first_command.set_args(["cat", "Bash-CLI/src/tests/data/numbers.txt"])
    pipe.append(first_command)

    second_command = Echo()
    second_command.set_args(["echo"])
    output = IOChannel()
    second_command.set_output_channel(output)
    pipe.append(second_command)

    pipe.execute()
    assert output.read() == '\n'


def test_cat_pass_to_pipe():
    pipe = Pipe()
    first_command = Cat()
    first_command.set_args(["cat", "Bash-CLI/src/tests/data/numbers.txt"])
    pipe.append(first_command)

    second_command = Cat()
    second_command.set_args(["cat"])
    output = IOChannel()
    second_command.set_output_channel(output)
    pipe.append(second_command)

    pipe.execute()
    assert output.read() == '3\n2\n1'


def test_pwd_to_pipe():
    pipe = Pipe()
    first_command = Pwd()
    first_command.set_args(["pwd"])
    pipe.append(first_command)

    second_command = Cat()
    second_command.set_args(["cat"])
    output = IOChannel()
    second_command.set_output_channel(output)
    pipe.append(second_command)

    pipe.execute()
    assert output.read() == os.getcwd() + '\n'


def test_pwd_not_read_from_pipe():
    pipe = Pipe()
    first_command = Echo()
    first_command.set_args(["echo", "1"])
    pipe.append(first_command)

    second_command = Pwd()
    second_command.set_args(["pwd"])
    output = IOChannel()
    second_command.set_output_channel(output)
    pipe.append(second_command)

    pipe.execute()
    assert output.read() == os.getcwd() + '\n'


def test_wc_from_pipe():
    pipe = Pipe()
    first_command = Echo()
    first_command.set_args(["echo", "1", "23"])
    pipe.append(first_command)

    second_command = Wc()
    second_command.set_args(["wc"])
    output = IOChannel()
    second_command.set_output_channel(output)
    pipe.append(second_command)

    pipe.execute()
    assert output.read() == "1 2 5\n"


def test_wc_to_pipe():
    pipe = Pipe()
    first_command = Wc()
    first_command.set_args(["wc", "Bash-CLI/src/tests/data/numbers.txt"])
    pipe.append(first_command)

    second_command = Cat()
    second_command.set_args(["cat"])
    output = IOChannel()
    second_command.set_output_channel(output)
    pipe.append(second_command)

    pipe.execute()
    assert output.read() == "3 3 5\n"


def test_external_from_pipe():
    pipe = Pipe()
    first_command = Cat()
    first_command.set_args(["cat", "Bash-CLI/src/tests/data/numbers.txt"])
    pipe.append(first_command)

    second_command = CallExternal()
    second_command.set_args(["sort"])
    output = IOChannel()
    second_command.set_output_channel(output)
    pipe.append(second_command)

    pipe.execute()
    assert output.read() == "1\n2\n3\n"


def test_external_to_pipe():
    pipe = Pipe()
    first_command = CallExternal()
    first_command.set_args(["sort", "Bash-CLI/src/tests/data/numbers.txt"])
    pipe.append(first_command)

    second_command = Cat()
    second_command.set_args(["cat"])
    output = IOChannel()
    second_command.set_output_channel(output)
    pipe.append(second_command)

    pipe.execute()
    assert output.read() == "1\n2\n3\n"
