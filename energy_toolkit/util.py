
from enum import Enum
import platform

class Datapoint():
   """Data class for managing measurement values inside the toolkit. Each datapoint stores the recorded energy and the duration of the execution"""
   energy: float = 0.0
   time: float = 0.0

   def __init__(self, eng, t):
      self.energy = eng
      self.time = t

class OS_TYPE(Enum):
    """OS enum to distinguish different types of OS"""
    LINUX = 1
    WINDOWS = 2
    UNSUPPORTED = 3

class CPU_TYPE(Enum):
    """CPU enum to distinguish different types of CPUs"""
    INTEL = 1
    AMD = 2
    UNSUPPORTED = 3

class Toolkit_Util:
  """Util class that provides several helper functions"""

  @staticmethod
  def get_OS() -> OS_TYPE:
    """Returns the type of the executing OS"""
    os_name = platform.system()
    if os_name == 'Windows':
      return OS_TYPE.WINDOWS
    elif os_name == 'Linux':
      return OS_TYPE.LINUX
    else:
      return OS_TYPE.UNSUPPORTED

  @staticmethod
  def get_cpu_vendor() -> CPU_TYPE:
    """Returns the CPU vendor of the executing device"""
    vendor = None
    with open('/proc/cpuinfo', 'r') as f:
      for line in f:
          if line.startswith('vendor_id'):
              vendor = line.split(':')[1].strip()

    if vendor:
      if 'GenuineIntel' in vendor:
          return CPU_TYPE.INTEL
      elif 'AuthenticAMD' in vendor:
          return CPU_TYPE.AMD
      else:
          return CPU_TYPE.UNSUPPORTED
    else:
        return CPU_TYPE.UNSUPPORTED    


