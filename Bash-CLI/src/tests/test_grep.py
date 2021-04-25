from bash.interpreter.builtins.grep import Grep
from bash.interpreter.channels.io_channel import IOChannel


def test_grep_match_single_line():
    text = "my input"
    pattern = "inp"

    input_channel = IOChannel()
    output_channel = IOChannel()
    command = Grep(pattern=pattern)
    command.set_input_channel(input_channel)
    command.set_output_channel(output_channel)
    input_channel.write(text)

    command.execute()

    assert output_channel.read() == "my input\n"


def test_grep_match_several_lines():
    text = "first line\nsecond\nline 3"
    pattern = "line"

    input_channel = IOChannel()
    output_channel = IOChannel()
    command = Grep(pattern=pattern)
    command.set_input_channel(input_channel)
    command.set_output_channel(output_channel)
    input_channel.write(text)

    command.execute()

    assert output_channel.read() == "first line\nline 3\n"


def test_grep_no_match():
    text = "first line\nsecond\nline 3"
    pattern = "no match"

    input_channel = IOChannel()
    output_channel = IOChannel()
    command = Grep(pattern=pattern)
    command.set_input_channel(input_channel)
    command.set_output_channel(output_channel)
    input_channel.write(text)

    command.execute()

    assert output_channel.read() == ""


def test_grep_to_stdout(capsys):
    text = "my input"
    pattern = "inp"

    input_channel = IOChannel()
    command = Grep(pattern=pattern)
    command.set_input_channel(input_channel)
    input_channel.write(text)

    command.execute()

    captured = capsys.readouterr()
    assert captured.out == "my input\n"


def test_grep_to_stdout_empty(capsys):
    text = "my input"
    pattern = "1"

    input_channel = IOChannel()
    command = Grep(pattern=pattern)
    command.set_input_channel(input_channel)
    input_channel.write(text)

    command.execute()

    captured = capsys.readouterr()
    assert captured.out == ""


def test_grep_ignore_case():
    text = "my iNput"
    pattern = "InP"

    input_channel = IOChannel()
    output_channel = IOChannel()
    command = Grep(pattern=pattern, ignore_case=True)
    command.set_input_channel(input_channel)
    command.set_output_channel(output_channel)
    input_channel.write(text)

    command.execute()

    assert output_channel.read() == "my iNput\n"


def test_grep_only_words_match():
    text = "my input"
    pattern = "my"

    input_channel = IOChannel()
    output_channel = IOChannel()
    command = Grep(pattern=pattern, only_words=True)
    command.set_input_channel(input_channel)
    command.set_output_channel(output_channel)
    input_channel.write(text)

    command.execute()

    assert output_channel.read() == "my input\n"


def test_grep_only_words_not_match():
    text = "my input"
    pattern = "inp"

    input_channel = IOChannel()
    output_channel = IOChannel()
    command = Grep(pattern=pattern, only_words=True)
    command.set_input_channel(input_channel)
    command.set_output_channel(output_channel)
    input_channel.write(text)

    command.execute()

    assert output_channel.read() == ""


def test_grep_lines_after():
    pattern = "3"

    output_channel = IOChannel()
    command = Grep(pattern=pattern, after_lines=1, file=open("Bash-CLI/src/tests/data/numbers.txt"))
    command.set_output_channel(output_channel)

    command.execute()

    assert output_channel.read() == "3\n2\n"


def test_grep_more_lines_than_in_file():
    pattern = "3"

    output_channel = IOChannel()
    command = Grep(pattern=pattern, after_lines=100, file=open("Bash-CLI/src/tests/data/numbers.txt"))
    command.set_output_channel(output_channel)

    command.execute()

    assert output_channel.read() == "3\n2\n1\n"


def test_all_flags_on():
    text = "FIRST line\nlIn2\nLINE 3\nlIn4\nlIn5"
    pattern = "lIne"

    input_channel = IOChannel()
    output_channel = IOChannel()
    command = Grep(pattern=pattern, ignore_case=True, only_words=True, after_lines=1)
    command.set_input_channel(input_channel)
    command.set_output_channel(output_channel)
    input_channel.write(text)

    command.execute()

    assert output_channel.read() == "FIRST line\nlIn2\nLINE 3\nlIn4\n"


def test_regexp_match():
    text = "first line\nsecond\nline 3"
    pattern = "f[i|r]*s.*"

    input_channel = IOChannel()
    output_channel = IOChannel()
    command = Grep(pattern=pattern)
    command.set_input_channel(input_channel)
    command.set_output_channel(output_channel)
    input_channel.write(text)

    command.execute()

    assert output_channel.read() == "first line\n"


def test_regexp_not_match():
    text = "first line\nsecond\nline 3"
    pattern = "f[i|r]*s.^[ ]*"

    input_channel = IOChannel()
    output_channel = IOChannel()
    command = Grep(pattern=pattern)
    command.set_input_channel(input_channel)
    command.set_output_channel(output_channel)
    input_channel.write(text)

    command.execute()

    assert output_channel.read() == ""


def test_grep_match_several_with_lines_after():
    pattern = "3|2"

    output_channel = IOChannel()
    command = Grep(pattern=pattern, after_lines=1, file=open("Bash-CLI/src/tests/data/numbers.txt"))
    command.set_output_channel(output_channel)

    command.execute()

    assert output_channel.read() == "3\n2\n1\n"
