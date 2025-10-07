import unittest
from energy_toolkit.energy_toolkit import Energy_Toolkit

class TestEnergyToolkit(unittest.TestCase):
    def setUp(self):
        """Setup for the tests to create an instance of the Energy_Toolkit class."""
        self.toolkit = Energy_Toolkit(dps=10, reps=5)

    def test_import(self):
        """Test the import of the Energy_Toolkit class."""
        self.assertIsInstance(self.toolkit, Energy_Toolkit)

    def test_add_program(self):
        """Test adding a program to the toolkit's program list."""
        self.toolkit.add_program('test_program')
        self.assertIn('test_program', self.toolkit._programs)

    def test_clear_programs(self):
        """Test clearing all programs from the toolkit's program list."""
        self.toolkit.add_program('program1')
        self.toolkit.add_program('program2')
        self.toolkit.clear_programs()
        self.assertEqual(len(self.toolkit._programs), 0)

if __name__ == '__main__':
    unittest.main()