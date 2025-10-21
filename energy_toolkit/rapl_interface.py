"""
RAPL register reader abstraction module.
Offers a singel method to read the energy values of the current system.
Selects different method depending on the present CPU vendor.
"""

from energy_toolkit.util import CPU_TYPE
from energy_toolkit import msr_reader


class RAPLInterface:
    """RAPL register reader abstraction class"""

    @staticmethod
    def read(vendor, core=0):
        """Reads the given core energy counter and returns it"""
        energy = None
        registerpath = f"/dev/cpu/{core}/msr"

        if vendor == CPU_TYPE.AMD:
            energy = msr_reader.read_amd_msr(registerpath)
        elif vendor == CPU_TYPE.INTEL:
            energy = msr_reader.read_intel_msr(registerpath)
        else:
            energy = RAPLInterface._read_armsilicon()

        return energy

    @staticmethod
    def _read_armsilicon():
        """Dummy function to provide values for apple silicon devices"""
        return 0.0
