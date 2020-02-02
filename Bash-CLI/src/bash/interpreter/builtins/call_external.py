import subprocess

from ..command import Command


class CallExternal(Command):
    """
    A call of an external command.
    The first argument is a name of the command, while other are passed as its arguments.
    If an environment is passed, updates the system environment before a call.
    """
    def __init__(self, environment=None):
        super().__init__()
        self.environment = environment

    def execute(self):
        try:
            process = self.__prepare_process()

            output_bytes = process.communicate()[0]
            process.stdin.close()

            output_string = self.__convert_bytes_to_string(output_bytes)
            self._output_channel.write(output_string)
        except subprocess.CalledProcessError as error:
            raise Exception(f'Failed to run external command. Command: '
                            f'{self._args[0]}, '
                            f'{self.__convert_bytes_to_string(error.stdout)}')

    def __prepare_process(self):
        process = subprocess.Popen(
            self._args,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        if self.environment:
            self.environment.update_system_environment()

        if self._input_channel:
            input_data_string = self._input_channel.read()
            input_data_bytes = self.__convert_string_to_bytes(input_data_string)
            process.stdin.write(input_data_bytes)
        return process

    def __convert_bytes_to_string(self, bytes):
        return str(bytes, "utf-8")

    def __convert_string_to_bytes(self, string):
        return string.encode('utf-8')
