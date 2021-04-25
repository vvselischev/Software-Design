from bash.interpreter.builtins.wc import Wc
from bash.interpreter.channels.io_channel import IOChannel


def test_wc_from_argument():
    command = Wc()
    output = IOChannel()
    command.set_args(["wc", "Bash-CLI/src/tests/data/example.txt"])
    command.set_output_channel(output)
    command.execute()

    expected = "3 4 21\n"
    assert output.read() == expected


def test_wc_to_stdout(capsys):
    command = Wc()
    command.set_args(["wc", "Bash-CLI/src/tests/data/example.txt"])
    command.execute()

    expected = "3 4 21\n"
    captured = capsys.readouterr()
    assert captured.out == expected


def test_wc_from_channel():
    command = Wc()
    input = IOChannel()
    input.write("my input")

    output = IOChannel()

    command.set_args(["cat"])
    command.set_output_channel(output)
    command.set_input_channel(input)
    command.execute()

    expected = "1 2 8\n"
    assert output.read() == expected
