import os

from bash.interpreter.builtins.pwd import Pwd
from bash.interpreter.channels.io_channel import IOChannel


def test_correct_directory():
    command = Pwd()
    command.set_args(["pwd"])
    output = IOChannel()
    command.set_output_channel(output)
    command.execute()

    assert output.read() == os.getcwd() + '\n'
