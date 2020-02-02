from bash.interpreter.interpreter import Interpreter


class Cli:
    """
    A command-line interface. Reads commands from the stdin and
    prints the result (if any) to stdout.
    Each new command must be written in one line.
    """
    def __init__(self):
        self.interpreter = Interpreter(self)
        self._running = False

    def start(self):
        """Starts the cli"""
        self._running = True

        while self._running:
            print("> ", end='')
            command = input()

            if len(command) == 0:
                continue

            try:
                self.interpreter.process(command)
            except Exception as exception:
                print(exception)

    def stop(self):
        """Stops the cli after the execution of the current command is finished."""
        self._running = False
