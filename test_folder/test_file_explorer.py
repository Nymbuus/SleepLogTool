import unittest
from unittest.mock import patch
from sleep_log_tool_repo.sleep_log_tool import SleepLogTool

class TestFileExplorer(unittest.TestCase):
    """ Testing file_explorer function. """

    def setUp(self):
        self._sleeplogtool = SleepLogTool()

    @patch("tkinter.filedialog.askopenfilenames", return_value=["SleepLogTool\\blf_testfiles\\Trace_BP11_Display_1_20240221_133700_20240221_133859_#08-1_LEM.blf"])
    def test_file_explorer_2min_file(self, mock_input):
        """ Tests if the opened file actualy returns the correct name. """
        actual_file_name = self._sleeplogtool.file_explorer()
        expected_file_name = ["SleepLogTool\\blf_testfiles\\Trace_BP11_Display_1_20240221_133700_20240221_133859_#08-1_LEM.blf"]
        self.assertEqual(expected_file_name, actual_file_name)

    @patch("tkinter.filedialog.askopenfilenames", return_value=["Sleeplogtool\\blf_testfiles\\Trace_BP11_Display_1_20240220_160600_20240221_062959_#08-1_LEM.blf"])
    def test_file_explorer_long_file(self, mock_input):
        """ Tests if the opened file actualy returns the correct name. """
        actual_file_name = self._sleeplogtool.file_explorer()
        expected_file_name = ["Sleeplogtool\\blf_testfiles\\Trace_BP11_Display_1_20240220_160600_20240221_062959_#08-1_LEM.blf"]
        self.assertEqual(expected_file_name, actual_file_name)

    @patch("tkinter.filedialog.askopenfilenames", return_value=["SleepLogTool\\blf_testfiles\\Trace_BP11_Display_1_20240221_133700_20240221_133859_#08-1_LEM.blf",
                                                                 "Sleeplogtool\\blf_testfiles\\Trace_BP11_Display_1_20240220_160600_20240221_062959_#08-1_LEM.blf"])
    def test_file_explorer_2files(self, mock_input):
        """ Tests if the opened file actualy returns the correct name. """
        actual_file_name = self._sleeplogtool.file_explorer()
        expected_file_name = ["SleepLogTool\\blf_testfiles\\Trace_BP11_Display_1_20240221_133700_20240221_133859_#08-1_LEM.blf",
                              "Sleeplogtool\\blf_testfiles\\Trace_BP11_Display_1_20240220_160600_20240221_062959_#08-1_LEM.blf"]
        self.assertEqual(expected_file_name, actual_file_name)
    
    @patch("tkinter.filedialog.askopenfilenames", return_value="")
    def test_file_explorer_no_file(self, mock_input):
        """ Tests if the opened file actualy returns the correct name. """
        with self.assertRaises(SystemExit):
            self._sleeplogtool.file_explorer()

    def tearDown(self):
        self._sleeplogtool = None
