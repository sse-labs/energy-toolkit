
"""_summary_
Program abstraction class, that models a program that can be executed.
"""
class Program:
  executeable = None
  arguments = None
  inputfile = None

  """_summary_
  Create a new Program object
  """
  def __init__(self, exe, args, inpfile):
    self.executeable = exe
    self.arguments = args
    self.inputfile = inpfile

  """_summary_
  Execute the program on a specific core
  """
  def execute(self, core = 0):
    pass