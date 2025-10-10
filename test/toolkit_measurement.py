from typing import Dict
import unittest

import numpy as np
from energy_toolkit.energy_toolkit import Energy_Toolkit, Program

class TestEnergyToolkitMeasurement(unittest.TestCase):
    toolkit: Energy_Toolkit = None
    result: Dict[str, np.ndarray] = None

    def setUp(self):
        """Initialize a toolkit with a measurement"""
        self.toolkit = Energy_Toolkit(10, 10)
        p = Program('./dummy_prog', [], "")
        self.toolkit.add_program(p)
        self.result = self.toolkit.measure()

    def test_measurement(self):
        """Check if a valid amount of datapoints was recorded"""
        datapoints = self.result.popitem()[1]
        self.assertEqual(len(datapoints), 10)

    def test_print_statistics(self):
        """Print statistics"""
        self.toolkit.print_statistics(self.result)
        

if __name__ == '__main__':
    unittest.main()