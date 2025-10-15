import time
from energy_toolkit.rapl_interface import RAPL_Interface
from typing import Dict, List
from energy_toolkit.program import Program
from energy_toolkit.logger import Logger
import numpy as np
import os

from energy_toolkit.util import Datapoint, Toolkit_Util

class Energy_Toolkit():
  """
  Main class of the energy-toolkit package. Provides multiple methods for measuring the energy of any given program
  """
  _datapoints = 0
  _repetitions = 0
  _core = 0

  _programs: List[Program]  = []

  _results: Dict[str, np.ndarray] = {}
  _statistics: Dict[str, np.ndarray] = {}

  _result_path = "./results"
  _logger = None

  def __init__(self, datapoints=100, repetitions=100, core = 0, programs = [], resultpath = "./results"):
    self._datapoints = datapoints
    self._repetitions = repetitions
    self._core = core
    self._programs = programs
    self._result_path = resultpath
    self._logger = Logger().get_logger()
    self._vendor = Toolkit_Util.get_cpu_vendor()

  def add_program(self, program: Program) -> None:
    """
    Add a new program to the list of programs to be executed
    """
    self._programs.append(program)

  def clear_programs(self) -> None:
    """
    Remove all programs from the list of programs to be executed
    """
    self._programs.clear()

  def measure(self) -> None:
    """
    Executes the programs added to the toolkit after another and measures the energy for each of the programs
    """

    # Dict to store relation program -> Datapoints
    program_energy_usage: Dict[str, List[Datapoint]] = {}

    for id, program in enumerate(self._programs):
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
            eng_before = RAPL_Interface.read(self._vendor)
            
            # Execute the current program
            program.execute(self._core)

            # Read time and energy counter after measurement
            eng_after = RAPL_Interface.read(self._vendor)
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
          prog_values.append(Datapoint(avg_eng, avg_time))

      # Store the datapoints recorded for the current program in our dict
      program_energy_usage[id] = prog_values
    

    # Convert our dict to dict -> numpy structure
    dtype = np.dtype([('energy', float), ('time', float)])

    arrays = {
      key: np.array([(dp.energy, dp.time) for dp in dplist], dtype=dtype)
      for key, dplist in program_energy_usage.items()
    }

    # Save measured results to the object
    self._results = arrays
    # Start statistics generation
    self._generate_statistics()


  def _generate_statistics(self) -> None:
    """Generate a statistics dict for further processing"""

    statistics = {}

    # Iterate over program ids in the given results
    for pid in self._results:
      program_stats = {}
      time_dict = {}
      energy_dict = {}

      time_values = self._results[pid]['time']
      energy_values = self._results[pid]['energy']

      # Call numpy statistic methods to calculate values
      time_dict["mean"] = time_values.mean()
      time_dict["variance"] = time_values.var()
      time_dict["std_deviation"] = time_values.std()

      energy_dict["mean"] = energy_values.mean()
      energy_dict["variance"] = energy_values.var()
      energy_dict["std_deviation"] = energy_values.std()

      program_stats["time"] = time_dict
      program_stats["energy"] = energy_dict

      statistics[pid] = program_stats
    
    self._statistics = statistics



  def print_statistics(self) -> None:
    """Prints some statistic metrics for the given results returned from a measurement"""
    
    # Iterate over program ids in the given results
    for pid in self._statistics:
      # Retrieve the actual program with the program id
      program: Program = self._programs[pid]

      time_values = self._statistics[pid]['time']
      energy_values = self._statistics[pid]['energy']

      output = f"""====================================
      Program {pid}: {program.executeable}

      Time:
        AVG: {time_values["mean"]:.5e} s
        VAR: {time_values["variance"]:.5e} s
        STD: {time_values["std_deviation"]:.5e} s

      Energy:
        AVG: {energy_values["mean"]:.5e} J
        VAR: {energy_values["variance"]:.5e} J
        STD: {energy_values["std_deviation"]:.5e} J
      ====================================
      """

      print(output)

  def get_results(self) -> Dict[str, np.ndarray]:
    """Return the currently saved results"""
    return self._results

  def get_statistics(self) -> Dict[str, Dict[str, float]]:
    """Return the currently saved statistics"""
    return self._statistics
  
  def _create_location_if_not_exists(self, location) -> bool:
    """Helper method that creates a folder at a location if it does not exists. If an error occurs an error message is printed"""
    try:
      # Check if the given path exists
      if not os.path.exists(location):
        # Create the given directory
        os.makedirs(location)

      return True
    except:
      # Catch any error prohibiting the creation of the folder
      self._logger.error("Creation of result location failed!")
      return False
    
  
  def write_results(self):
    """Write the last saved results to a file. One file for each program under analysis at the specific result location"""
    folder_successfully_created = self._create_location_if_not_exists(self._result_path)

    if folder_successfully_created:
      # iterate over the saved results
      for pid in self._results:
        # Convert custom dict to a numpy array
        data = np.column_stack((self._results[pid]['time'], self._results[pid]['energy']))

        # Construct the pid folder inside the results dir
        savefolder = os.path.join(self._result_path, str(pid))
        pid_folder_created = self._create_location_if_not_exists(savefolder)

        if pid_folder_created:
          savelocation = os.path.join(savefolder, "results.csv")
          # Save our data as .csv file at the result location
          np.savetxt(savelocation, data, header='Time,Energy', delimiter=',', fmt='%s')
        else:
          self._logger.error("File could not be saved! Do you habe the correct rights to access the result location?")

    else:
      self._logger.error("File could not be saved! Do you habe the correct rights to access the result location?")


  def write_statistics(self):
    """Write the last saved statistics to a file. One file for each program under analysis at the specific result location"""
    folder_successfully_created = self._create_location_if_not_exists(self._result_path) # create the result location if it does not exist

    if folder_successfully_created:
      # iterate over the saved results
      for pid in self._results:
        # Convert custom dict to a numpy array
        data = np.column_stack((
          ["mean", "variance", "std_deviation"],
          list(self._statistics[pid]['time'].values()),
          list( self._statistics[pid]['energy'].values())
          ))

        # Construct the pid folder inside the results dir
        savefolder = os.path.join(self._result_path, str(pid))
        pid_folder_created = self._create_location_if_not_exists(savefolder)

        if pid_folder_created:
          savelocation = os.path.join(savefolder, "statistics.csv")
          # Save our data as .csv file at the result location
          np.savetxt(savelocation, data, header='Value,Time,Energy', delimiter=',', fmt='%s')
        else:
          self._logger.error("File could not be saved! Do you habe the correct rights to access the result location?")

    else:
      self._logger.error("File could not be saved! Do you habe the correct rights to access the result location?")
