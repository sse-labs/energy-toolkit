from typing import Dict
import unittest

import numpy as np
from energy_toolkit.energy_toolkit import Energy_Toolkit, Program


class TestEnergyToolkitMeasurement(unittest.TestCase):
    toolkit: Energy_Toolkit = None
    result: Dict[str, np.ndarray] = None

    @classmethod
    def setUpClass(cls):
        """Initialize a toolkit with a measurement"""
        cls.toolkit = Energy_Toolkit(3, 2)
        p = Program("./dummyprog", [], "")
        cls.toolkit.add_program(p)
        cls.toolkit.measure()
        cls.result = cls.toolkit.get_results()

    def test_measurement(self):
        """Check if a valid amount of datapoints was recorded"""
        datapoints = self.result[0]
        self.assertEqual(len(datapoints), 3)

    def test_print_statistics(self):
        """Print statistics"""
        self.toolkit.print_statistics()

    def test_write_result(self):
        """Write results"""
        self.toolkit.write_results()

    def test_write_statistics(self):
        """Write statistics"""
        self.toolkit.write_statistics()


if __name__ == "__main__":
    unittest.main()
