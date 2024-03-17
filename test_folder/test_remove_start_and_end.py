import unittest
from unittest.mock import patch
from sleep_log_tool_repo.sleep_log_tool import SleepLogTool

class TestRemoveStartAndEnd(unittest.TestCase):
    """ remove_start_and_end in sleep_log_tool.py """

    def setUp(self):
        self._sleeplogtool = SleepLogTool()

    @patch("sleep_log_tool_repo.sleep_log_tool.SleepLogTool.remove_start_get_input", return_value=1)
    def test_remove_start_get_input_int(self, mock_input):
        self.assertEqual(type(self._sleeplogtool.remove_start_get_input("hejsan")), int)

    @patch('builtins.input', return_value="aa")
    def test_remove_start_get_input_invalid_input(self, mock_input):
        with self.assertRaises(ValueError):
            self._sleeplogtool.remove_start_get_input("_")
            # Kollar om funktionen klarar av string input.

    def tearDown(self):
        self._sleeplogtool = None

if __name__ == "__main__":
    unittest.main()