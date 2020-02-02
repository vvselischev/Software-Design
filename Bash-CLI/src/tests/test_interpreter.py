from bash.controller import Cli
from bash.interpreter.interpreter import Interpreter


def test_single_command(capsys):
    cli = Cli()
    interpreter = Interpreter(cli)
    interpreter.process("echo 1")

    captured = capsys.readouterr()
    assert captured.out == "1\n"


def test_pipe(capsys):
    cli = Cli()
    interpreter = Interpreter(cli)
    interpreter.process("echo 123 | wc | cat")

    captured = capsys.readouterr()
    assert captured.out == "1 1 4\n"


def test_saves_environment(capsys):
    cli = Cli()
    interpreter = Interpreter(cli)
    interpreter.process("var1=1")
    interpreter.process("var2=2")
    interpreter.process("echo $var1 $var2")

    captured = capsys.readouterr()
    assert captured.out == "1 2\n"


def test_substitution_to_command(capsys):
    cli = Cli()
    interpreter = Interpreter(cli)
    interpreter.process("var1=ec")
    interpreter.process("var2=\"ho 1\"")
    interpreter.process("$var1$var2")

    captured = capsys.readouterr()
    assert captured.out == "1\n"
