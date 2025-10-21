"""
Util module that offers several helper classes and functions
"""

from enum import Enum
import platform
import cpuinfo


class Datapoint:
    """Data class for managing measurement values inside the toolkit. 
    Each datapoint stores the recorded energy and the duration of the execution"""

    energy: float = 0.0
    time: float = 0.0

    def __init__(self, eng, t):
        self.energy = eng
        self.time = t


class OS_TYPE(Enum): # pylint: disable=invalid-name
    """OS enum to distinguish different types of OS"""

    LINUX = 1
    WINDOWS = 2
    UNSUPPORTED = 3


class CPU_TYPE(Enum): # pylint: disable=invalid-name
    """CPU enum to distinguish different types of CPUs"""

    INTEL = 1
    AMD = 2
    APPLESILICON = 3
    UNSUPPORTED = 4


class ToolkitUtil:
    """Util class that provides several helper functions"""

    @staticmethod
    def get_OS() -> OS_TYPE: # pylint: disable=invalid-name
        """Returns the type of the executing OS"""
        os_name = platform.system()
        if os_name == "Windows":
            return OS_TYPE.WINDOWS

        if os_name == "Linux":
            return OS_TYPE.LINUX

        return OS_TYPE.UNSUPPORTED

    @staticmethod
    def get_cpu_vendor() -> CPU_TYPE:
        """Returns the CPU vendor of the executing device"""
        info = cpuinfo.get_cpu_info()

        brand = info["brand_raw"].lower()

        if brand:
            if "intel" in brand:
                return CPU_TYPE.INTEL

            if "amd" in brand:
                return CPU_TYPE.AMD

            if "apple" in brand or "m1" in brand or "m2" in brand or "m4" in brand:
                return CPU_TYPE.APPLESILICON

            return CPU_TYPE.UNSUPPORTED

        return CPU_TYPE.UNSUPPORTED
