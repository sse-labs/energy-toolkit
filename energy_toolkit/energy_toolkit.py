import time
from energy_toolkit.rapl_interface import RAPL_Interface
from typing import Dict, List
from energy_toolkit.program import Program
import numpy as np

from energy_toolkit.util import Datapoint

class Energy_Toolkit():
  """
  Main class of the energy-toolkit package. Provides multiple methods for measuring the energy of any given program
  """
  _datapoints = 0
  _repetitions = 0
  _core = 0

  _programs: List[Program]  = []

  def __init__(self, dps, reps, core = 0, programs = []):
    self._datapoints = dps
    self._repetitions = reps
    self._core = core
    self._programs = programs

  def add_program(self, program) -> None:
    """
    Add a new program to the list of programs to be executed
    """
    self._programs.append(program)

  def clear_programs(self) -> None:
    """
    Remove all programs from the list of programs to be executed
    """
    self._programs.clear()

  def measure(self) -> Dict[str, List[Datapoint]]:
    """
    Executes the programs added to the toolkit after another and measures the energy for each of the programs
    """

    # Dict to store relation program -> Datapoints
    program_energy_usage: Dict[str, List[Datapoint]] = {}

    for program in self._programs:
      # Store the recorded datapoint objects for each program separately
      prog_values: List[Datapoint] = []

      # Record 0 up to self._datapoints many average measurements
      for _ in range(0, self._datapoints):
          # Store the values recorded during each measurement repetition
          energy_per_rep = []
          time_per_rep = []

          # Record 0 up to self._repetitions many repetitions
          for _ in range(0, self._repetitions):
            # Take the current timer and energy reading
            time_before = time.perf_counter()
            eng_before = RAPL_Interface.read()
            
            # Execute the current program
            program.execute(self._core)

            # Read time and energy counter after measurement
            eng_after = RAPL_Interface.read()
            time_after = time.perf_counter()

            # TODO: We should add a way to repeat the last measurement, if the energy delta becomes negative. This would mitigate overflows in the datapoints.

            # Calculate the delta of each counter
            energy_cost = eng_after - eng_before
            duration = time_after - time_before

            # Add the measured energy and time readings to our repetition collection
            energy_per_rep.append(energy_cost)
            time_per_rep.append(duration)

          # Convert readings to numpy arrays
          np_energ = np.array(energy_per_rep)
          np_time = np.array(time_per_rep)

          # Calculate mean over the recorded values
          avg_eng = np.mean(np_energ)
          avg_time = np.mean(np_time)

          # Create and append a new datapoint object to our list of datapoints for the current program
          prog_values.append({avg_eng, avg_time})
    
      # Store the datapoints recorded for the current program in our dict
      program_energy_usage[program] = prog_values

    return program_energy_usage



    

