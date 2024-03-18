import unittest
from unittest.mock import patch
from sleep_log_tool_repo.sleep_log_tool import SleepLogTool
import pandas as pd
import csv

class TestRemoveTime(unittest.TestCase):
    """ Tests the function remove_time """

    def setUp(self):
        self._sleeplogtool = SleepLogTool()

        

    @patch("builtins.input", side_effect=["0", "0"])
    def test_remove_time_return(self, mock_input):
        """ Tests if remove_time function works as intended by entering '0' in both remove_start and remove_end.
            This test needs the files 'expected_test_file.csv' and 'actual_original_test_file.csv' to work. """
        expected_file_path = r"C:\SleepLogTool_Examensarbete\expected_test_file.csv"
        with open(expected_file_path, newline='') as csvfile:
            expected = [row for row in csv.DictReader(csvfile)]


        actual_original_file_path = r"C:\SleepLogTool_Examensarbete\actual_original_test_file.csv"
        df = self._sleeplogtool.csv_to_panda(actual_original_file_path)
        pd_df = pd.DataFrame(self._sleeplogtool.remove_time(df))
        actual_modified_file_path = r"C:\SleepLogTool_Examensarbete\actual_modified_test_file.csv"
        pd_df.to_csv(actual_modified_file_path, index=False, float_format="%.6f")

        with open(actual_modified_file_path, newline='') as csvfile:
            actual = [row for row in csv.DictReader(csvfile)]

        self.assertEqual(expected, actual)

    def tearDown(self):
        self._sleeplogtool = None