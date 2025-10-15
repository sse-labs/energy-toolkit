"""
RAPL register reader abstraction module.
Offers a singel method to read the energy values of the current system.
Selects different method depending on the present CPU vendor.
"""

import struct

from energy_toolkit.util import CPU_TYPE


class RAPLInterface: # pylint: disable=too-few-public-methods
    """RAPL register reader abstraction class"""

    @staticmethod
    def read(vendor, core=0):
        """Reads the given core energy counter and returns it"""
        energy = None
        registerpath = f"/dev/cpu/{core}/msr"

        if vendor == CPU_TYPE.AMD:
            energy = RAPLInterface._read_amd(registerpath)
        elif vendor == CPU_TYPE.INTEL:
            energy = RAPLInterface._read_intel(registerpath)
        else:
            energy = RAPLInterface._read_armsilicon()

        return energy

    @staticmethod
    def _read_intel(registerpath):
        """Reads the current energy register on an INTEL CPU and returns the current energy 
        register value in Joule"""
        energyreg = 0x639
        unitreg = 0x606

        energy = 0
        unit = 0

        with open(registerpath, "rb") as rf:
            rf.seek(energyreg)
            rawenergy = rf.read(8)
            energy = struct.unpack("Q", rawenergy)
            cleaned_energy = energy[0]

            rf.seek(0)
            rf.seek(unitreg)
            rawunit = rf.read(8)
            unit = struct.unpack("Q", rawunit)[0]
            cleaned_unit = (unit >> 8) & 0x1F

        return cleaned_energy * pow(0.5, cleaned_unit)

    @staticmethod
    def _read_amd(registerpath):
        """Reads the current energy register on an AMD CPU and returns the current energy 
        register value in Joule"""
        energyreg = 0xC001029A
        unitreg = 0xC0010299

        energy = 0
        unit = 0

        with open(registerpath, "rb") as rf:
            rf.seek(energyreg)
            rawenergy = rf.read(8)
            energy = struct.unpack("Q", rawenergy)
            cleaned_energy = energy[0]

            rf.seek(0)
            rf.seek(unitreg)
            rawunit = rf.read(8)
            unit = struct.unpack("Q", rawunit)[0]
            cleaned_unit = (unit >> 8) & 0x1F

        return cleaned_energy * pow(0.5, cleaned_unit)

    @staticmethod
    def _read_armsilicon():
        """Dummy function to provide values for apple silicon devices"""
        return 0.0
