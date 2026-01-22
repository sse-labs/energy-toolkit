"""
Program abstraction
"""
import os
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
        try:
            Logger().get_logger().debug(
                "Different way to call subprocess...",
            )
            fin = open(self._inputfile, "r") if self._inputfile else subprocess.DEVNULL

            subprocess.run(
                ["taskset", "-c", str(core), self._executeable] + self._arguments,
                stdin=fin,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=lambda: os.sched_setaffinity(0, {core}),
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
