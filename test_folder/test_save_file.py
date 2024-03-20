import unittest
from unittest.mock import patch, MagicMock
from sleep_log_tool_repo.sleep_log_tool import SleepLogTool

class TestSaveFile(unittest.TestCase):
    """ Tests the save_file function in sleep_log_tool. """

    def setUp(self):
        self._slt = SleepLogTool()

    @patch('tkinter.filedialog.asksaveasfile')
    def test_save_file_pass(self, mock_file_dialog):
        """ Tests the function to see if it works """
        mock_file_dialog.return_value = MagicMock(name='file_dialog')
        mock_file_dialog.return_value.name = 'SleepLogTool\\blf_testfiles\\save_file_test.csv'

        actual_result = self._slt.save_file()
        expected_result = 'SleepLogTool\\blf_testfiles\\save_file_test.csv'

        self.assertEqual(actual_result, expected_result)

        # Assert that asksaveasfile was called
        mock_file_dialog.assert_called_once_with(mode='w', defaultextension=".csv")


    @patch('tkinter.filedialog.asksaveasfile', return_value=None)
    def test_save_file_cancel(self, mock_file_dialog):
        """ Tests that the function exits the program if user cancels the interactive window. """
        with self.assertRaises(SystemExit):
            self._slt.save_file()

    def tearDown(self):
        self._slt = None
