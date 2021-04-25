from bash.interpreter.builtins.cat import Cat
from bash.interpreter.channels.io_channel import IOChannel


def test_cat_from_argument():
    command = Cat()
    output = IOChannel()
    command.set_args(["cat", "Bash-CLI/src/tests/data/example.txt"])
    command.set_output_channel(output)
    command.execute()

    expected = "first line\nsecond\n123"
    assert output.read() == expected


def test_cat_to_stdout(capsys):
    command = Cat()
    command.set_args(["cat", "Bash-CLI/src/tests/data/example.txt"])
    command.execute()

    expected = "first line\nsecond\n123"
    captured = capsys.readouterr()
    assert captured.out == expected


def test_cat_from_channel():
    command = Cat()
    input = IOChannel()
    input.write("my input")

    output = IOChannel()

    command.set_args(["cat"])
    command.set_output_channel(output)
    command.set_input_channel(input)
    command.execute()

    expected = "my input"
    assert output.read() == expected