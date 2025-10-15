"""
Program abstraction
"""

import subprocess

from energy_toolkit.logger import Logger

class Program:
    """
    Program abstraction class, that models a program that can be executed.
    """

    _executeable = None
    _arguments = None
    _inputfile = None

    def __init__(self, exe: str, args: list[str] = None, inpfile: str = ""):
        """
        Create a new Program object
        """
        self._executeable = exe

        if args is None:
            self._arguments = []
        else:
            self._arguments = args

        self._inputfile = inpfile

    def execute(self, core=0):
        """
        Execute the program on a specific core
        """
        arguments = " ".join(self._arguments)
        ex = self._executeable

        if self._inputfile:
            command = f"taskset -c {core} {ex} {arguments} < {self._inputfile} > /dev/null"
        else:
            command = f"taskset -c {core} {ex} {arguments} > /dev/null"

        try:
            subprocess.run(
                command,
                shell=True,           # Needed to use `<`
                capture_output=True,   # Capture stdout and stderr
                text=True,              # Get output as string
                check=True
            )

        except Exception as e: # pylint: disable=broad-exception-caught
            Logger().get_logger().error(e)

    def get_executeable(self):
        """Return the executeable attribute"""
        return self._executeable

    def get_arguments(self):
        """Return the arguments attribute"""
        return self._arguments

    def get_inputfile(self):
        """Return the inputfile attribute"""
        return self._inputfile
