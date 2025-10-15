import unittest
from energy_toolkit.rapl_interface import RAPL_Interface


class TestRAPLInterface(unittest.TestCase):

    def test_simple_read(self):
        """Test reading the RAPL interface"""
        self.assertIsNotNone(RAPL_Interface.read())


if __name__ == "__main__":
    unittest.main()
