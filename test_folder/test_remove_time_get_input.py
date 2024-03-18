import unittest
from unittest.mock import patch
from sleep_log_tool_repo.sleep_log_tool import SleepLogTool

class TestRemoveStartAndEnd(unittest.TestCase):
    """ Test for remove_time_get_input function in sleep_log_tool.py """

    def setUp(self):
        self._sleeplogtool = SleepLogTool()

    @patch("sleep_log_tool_repo.sleep_log_tool.SleepLogTool.remove_time_get_input", return_value=1)
    def test_time_get_input_int(self, mock_input):
        """ Checks if the function handles a integer input correctly. """
        self.assertEqual(type(self._sleeplogtool.remove_time_get_input("_")), int)

    @patch("builtins.input", return_value="aa")
    def test_time_get_input_string(self, mock_input):
        """ Checks if the function can handle string input. """
        with self.assertRaises(ValueError):
            self._sleeplogtool.remove_time_get_input("_")

    @patch("builtins.input", return_value="True")
    def test_time_get_input_True(self, mock_input):
        """ Checks if the function can handle a string input containing "True". """
        with self.assertRaises(ValueError):
            self._sleeplogtool.remove_time_get_input("_")

    def tearDown(self):
        self._sleeplogtool = None

if __name__ == "__main__":
    unittest.main()