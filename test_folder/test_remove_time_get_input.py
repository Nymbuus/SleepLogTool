import unittest
from unittest.mock import patch
from sleep_log_tool_repo.sleep_log_tool import SleepLogTool

class TestRemoveStartAndEnd(unittest.TestCase):
    """ Test for remove_time_get_input function in sleep_log_tool.py """

    def setUp(self):
        self._sleeplogtool = SleepLogTool()

    @patch("builtins.input", side_effect=["1"])
    def test_time_get_input_int(self, mock_input):
        """ Checks if the function handles a integer input correctly. """
        self.assertEqual(type(self._sleeplogtool.remove_time_get_input("_", 12000)), float)

    @patch("builtins.input", side_effect=["0.1"])
    def test_time_get_input_float(self, mock_input):
        """ Checks if the function handles a float input correctly. """
        self.assertEqual(type(self._sleeplogtool.remove_time_get_input("_", 12000)), float)
        
    @patch("builtins.input", side_effect=["1"])
    def test_time_get_input_1(self, mock_input):
        """ Checks if the function actually returns 1. """
        self.assertEqual(self._sleeplogtool.remove_time_get_input("_", 12000), 1)

    @patch("builtins.input", side_effect=["aa", "1"])
    def test_time_get_input_string(self, mock_input):
        """ Checks if the function can handle string input. """
        self.assertEqual(type(self._sleeplogtool.remove_time_get_input("_", 12000)), float)

    @patch("builtins.input", side_effect=["True", "1"])
    def test_time_get_input_True(self, mock_input):
        """ Checks if the function can handle a string input containing "True". """
        self.assertEqual(type(self._sleeplogtool.remove_time_get_input("_", 12000)), float)
    
    @patch("builtins.input", side_effect=["-1", "1"])
    def test_time_get_input_negative(self, mock_input):
        """ Checks if the function can handle negative numbers. """
        self.assertEqual(type(self._sleeplogtool.remove_time_get_input("_", 12000)), float)

    @patch("builtins.input", side_effect=["3", "1"])
    def test_time_get_input_too_high(self, mock_input):
        """ Checks if the function can handle a number too high for the file selected. """
        self.assertEqual(type(self._sleeplogtool.remove_time_get_input("_", 12000)), float)
    
    @patch("builtins.input", side_effect=["1.5", "1.5", "0.4"])
    def test_time_get_input_second_value_too_high(self, mock_input):
        """ Checks if the second input is too high. """
        removed_time = self._sleeplogtool.remove_time_get_input("_",12000)
        self.assertEqual(type(self._sleeplogtool.remove_time_get_input("_", 12000 - (removed_time * 6000))), float)

    def tearDown(self):
        self._sleeplogtool = None

if __name__ == "__main__":
    unittest.main()