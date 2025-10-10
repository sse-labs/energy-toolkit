
import struct

from energy_toolkit.util import Toolkit_Util
from energy_toolkit.util import CPU_TYPE


class RAPL_Interface:
  
  @staticmethod
  def read(core=0):
    """Reads the given core energy counter and returns it"""
    energy = None
    registerpath = f"/dev/cpu/{core}/msr"

    if Toolkit_Util.get_cpu_vendor() == CPU_TYPE.AMD:
      energy = RAPL_Interface._read_amd(registerpath)
    elif Toolkit_Util.get_cpu_vendor() == CPU_TYPE.INTEL:
      energy = RAPL_Interface._read_intel(registerpath)
    else:
      energy = RAPL_Interface._read_armsilicon()
    
    return energy
  
  def _read_intel(registerpath):
    """Reads the current energy register on an INTEL CPU and returns the current energy register value in Joule"""
    energyreg = 0x639
    unitreg = 0x606

    energy = 0
    unit = 0

    with open(registerpath, 'rb') as rf:
      rf.seek(energyreg)
      rawenergy = rf.read(8)
      energy = struct.unpack('Q', rawenergy)
      cleaned_energy = energy[0]

      rf.seek(0)
      rf.seek(unitreg)
      rawunit = rf.read(8)
      unit = struct.unpack('Q', rawunit)[0]
      cleaned_unit = (unit >> 8) & 0x1F

    return cleaned_energy * pow(0.5, cleaned_unit)

  def _read_amd(registerpath):
    """Reads the current energy register on an AMD CPU and returns the current energy register value in Joule"""
    energyreg = 0xC001029A
    unitreg = 0xC0010299

    energy = 0
    unit = 0

    with open(registerpath, 'rb') as rf:
      rf.seek(energyreg)
      rawenergy = rf.read(8)
      energy = struct.unpack('Q', rawenergy)
      cleaned_energy = energy[0]

      rf.seek(0)
      rf.seek(unitreg)
      rawunit = rf.read(8)
      unit = struct.unpack('Q', rawunit)[0]
      cleaned_unit = (unit >> 8) & 0x1F

    return cleaned_energy * pow(0.5, cleaned_unit)

  def _read_armsilicon():
    return 0.0