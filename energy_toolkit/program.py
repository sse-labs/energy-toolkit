
class Program:
  """
  Program abstraction class, that models a program that can be executed.
  """
  executeable = None
  arguments = None
  inputfile = None

  def __init__(self, exe, args, inpfile):
    """
    Create a new Program object
    """
    self.executeable = exe
    self.arguments = args
    self.inputfile = inpfile

  def execute(self, core = 0):
    """
    Execute the program on a specific core
    """
    pass