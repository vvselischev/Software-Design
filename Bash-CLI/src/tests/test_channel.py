from bash.interpreter.channels.io_channel import IOChannel
from bash.interpreter.channels.stdout_channel import StdoutChannel


def test_single_io():
    channel = IOChannel()
    channel.write("value")
    output = channel.read()
    assert output == "value"


def test_multiple_write():
    channel = IOChannel()
    channel.write("1")
    channel.write("2")
    channel.write("3")
    output = channel.read()
    assert output == "123"


def test_multiple_read():
    channel = IOChannel()
    channel.write("1")
    output = channel.read()
    assert output == "1"

    output = channel.read()
    assert output == "1"


def test_mixed():
    channel = IOChannel()
    channel.write("1")
    output = channel.read()
    assert output == "1"
    channel.write("2")
    output = channel.read()
    assert output == "12"


def test_stdout_channel(capsys):
    channel = StdoutChannel()
    channel.write("my output")
    captured = capsys.readouterr()
    assert captured.out == "my output"
