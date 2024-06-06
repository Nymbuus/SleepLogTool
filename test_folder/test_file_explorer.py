import unittest
from unittest.mock import patch
from modules.files_preperation import FilesPreperation

SHORT_BLF = ["SleepLogTool\\blf_testfiles\\Trace_BP11_Display_1_20240221_133700_20240221_133859_#08-1_LEM.blf"]
LONG_BLF = ["Sleeplogtool\\blf_testfiles\\Trace_BP11_Display_1_20240220_160600_20240221_062959_#08-1_LEM.blf"]

class TestFileExplorer(unittest.TestCase):
    """ Testing file_explorer function. """

    def setUp(self):
        self._fp = FilesPreperation()

    @patch("tkinter.filedialog.askopenfilenames", return_value=SHORT_BLF)
    def test_file_explorer_2min_file(self, mock_input):
        """ Tests if the opened file actualy returns the correct name. """
        actual_file_name = self._fp.file_explorer()
        expected_file_name = SHORT_BLF
        self.assertEqual(expected_file_name, actual_file_name)

    @patch("tkinter.filedialog.askopenfilenames", return_value=LONG_BLF)
    def test_file_explorer_long_file(self, mock_input):
        """ Tests if the opened file actualy returns the correct name. """
        actual_file_name = self._fp.file_explorer()
        expected_file_name = LONG_BLF
        self.assertEqual(expected_file_name, actual_file_name)

    @patch("tkinter.filedialog.askopenfilenames", return_value=SHORT_BLF + LONG_BLF)
    def test_file_explorer_2files(self, mock_input):
        """ Tests if the opened file actualy returns the correct name. """
        actual_file_name = self._fp.file_explorer()
        expected_file_name = SHORT_BLF + LONG_BLF
        self.assertEqual(expected_file_name, actual_file_name)

    def tearDown(self):
        self._fp = None
