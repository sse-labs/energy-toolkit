import unittest
from energy_toolkit.energy_toolkit import Energy_Toolkit


class TestEnergyToolkitClass(unittest.TestCase):
    toolkit: Energy_Toolkit = None

    def setUp(self):
        self.toolkit = Energy_Toolkit()

    def test_creation(self):
        """Test creation of the toolkit"""
        tkt = Energy_Toolkit()
        self.assertIsNotNone(tkt)

    def test_parameter(self):
        """Test measurement parameters"""
        tkt = Energy_Toolkit()
        self.assertEqual(tkt._datapoints, 100)
        self.assertEqual(tkt._repetitions, 100)

        tkt = Energy_Toolkit(datapoints=50, repetitions=42)
        self.assertEqual(tkt._datapoints, 50)
        self.assertEqual(tkt._repetitions, 42)

    def test_add_program(self):
        """Test adding a program to the toolkit's program list."""
        self.toolkit.add_program("test_program")
        self.assertIn("test_program", self.toolkit._programs)

    def test_clear_programs(self):
        """Test clearing all programs from the toolkit's program list."""
        self.toolkit.add_program("program1")
        self.toolkit.add_program("program2")
        self.toolkit.clear_programs()
        self.assertEqual(len(self.toolkit._programs), 0)


if __name__ == "__main__":
    unittest.main()
