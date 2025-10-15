"""
Program abstraction
"""

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
        self.executeable = exe
        self.arguments = args
        self.inputfile = inpfile

    def execute(self, core=0):
        """
        Execute the program on a specific core
        """
        print(core)

    def get_executeable(self):
        """Return the executeable attribute"""
        return self._executeable

    def get_arguments(self):
        """Return the arguments attribute"""
        return self._arguments

    def get_inputfile(self):
        """Return the inputfile attribute"""
        return self._inputfile
