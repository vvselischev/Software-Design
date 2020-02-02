import pytest

from bash.interpreter.builtins.call_external import CallExternal
from bash.interpreter.channels.io_channel import IOChannel


def test_external_to_channel():
    command = CallExternal()
    command.set_args(["git", "--help"])
    output = IOChannel()
    command.set_output_channel(output)
    command.execute()

    actual = output.read()
    assert actual[:5] == "usage"


def test_external_from_channel():
    command = CallExternal()
    command.set_args(["sort"])
    output = IOChannel()
    input = IOChannel()
    input.write("3\n2\n1\n")

    command.set_input_channel(input)
    command.set_output_channel(output)
    command.execute()

    expected = "1\n2\n3\n"
    assert output.read() == expected


def test_external_ignores_stdin():
    command = CallExternal()
    command.set_args(["echo", "1"])
    output = IOChannel()
    input = IOChannel()
    input.write("input")

    command.set_input_channel(input)
    command.set_output_channel(output)
    command.execute()

    expected = "1\n"
    assert output.read() == expected



def test_external_with_many_args():
    command = CallExternal()
    command.set_args(["echo", "1", "2", "3"])
    output = IOChannel()
    command.set_output_channel(output)
    command.execute()

    expected = "1 2 3\n"
    assert output.read() == expected


def test_external_with_no_args():
    command = CallExternal()
    command.set_args(["echo"])
    output = IOChannel()
    command.set_output_channel(output)
    command.execute()

    expected = "\n"
    assert output.read() == expected


def test_external_to_stdout(capsys):
    command = CallExternal()
    command.set_args(["git", "--help"])
    command.execute()

    captured = capsys.readouterr()
    assert captured.out[:5] == "usage"


def test_external_not_found():
    command = CallExternal()
    command.set_args(["команда_не_найдена"])

    with pytest.raises(Exception):
        command.execute()
