

class Energy_Toolkit():
  """
  Main class of the energy-toolkit package. Provides multiple methods for measuring the energy of any given program
  """
  _datapoints = 0
  _repetitions = 0
  _core = 0

  _programs = []

  def __init__(self, dps, reps, core = 0, programs = []):
    self._datapoints = dps
    self._repetitions = reps
    self._core = core
    self._programs = programs

  def add_program(self, program):
    """
    Add a new program to the list of programs to be executed
    """
    self._programs.append(program)

  def clear_programs(self):
    """
    Remove all programs from the list of programs to be executed
    """
    self._programs.clear()

  def measure(self):
    """
    Executes the programs added to the toolkit after another and measures the energy for each of the programs
    """
    pass

