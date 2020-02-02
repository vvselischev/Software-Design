import io

from bash.interpreter.builtins.echo import Echo
from bash.interpreter.channels.io_channel import IOChannel


def test_echo_empty():
    command = Echo()
    output = IOChannel()
    command.set_args(["echo"])
    command.set_output_channel(output)
    command.execute()

    expected = "\n"
    assert output.read() == expected


def test_echo_simple():
    command = Echo()
    output = IOChannel()
    command.set_args(["echo", "123"])
    command.set_output_channel(output)
    command.execute()

    expected = "123\n"
    assert output.read() == expected


def test_echo_several():
    command = Echo()
    output = IOChannel()
    command.set_args(["echo", "my", "input"])
    command.set_output_channel(output)
    command.execute()

    expected = "my input\n"
    assert output.read() == expected


def test_echo_to_stdout(capsys):
    command = Echo()
    command.set_args(["echo", "my input"])
    command.execute()

    expected = "my input\n"
    captured = capsys.readouterr()
    assert captured.out == expected


def test_echo_ignores_input_channel():
    command = Echo()
    input = IOChannel()
    input.write("my input")

    output = IOChannel()

    command.set_args(["echo"])
    command.set_output_channel(output)
    command.set_input_channel(input)
    command.execute()

    expected = "\n"
    assert output.read() == expected
