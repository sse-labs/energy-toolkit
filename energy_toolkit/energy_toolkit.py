

"""_summary_
Main class of the energy-toolkit package. Provides multiple methods for measuring the energy of any given program
"""
class Energy_Toolkit():
  _datapoints = 0
  _repetitions = 0
  _core = 0

  _programs = []

  def __init__(self, dps, reps, core = 0, programs = []):
    self._datapoints = dps
    self._repetitions = reps
    self._core = core
    self._programs = programs

  """_summary_
  Add a new program to the list of programs to be executed
  """
  def add_program(self, program):
    self._programs.append(program)

  """_summary_
  Remove all programs from the list of programs to be executed
  """
  def clear_programs(self):
    self._programs.clear()

  """_summary_
  Executes the programs added to the toolkit after another and measures the energy for each of the programs
  """
  def measure(self):
    pass

