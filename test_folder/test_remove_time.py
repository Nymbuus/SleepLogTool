import unittest
from unittest.mock import patch
import pandas as pd
import csv
from SleepLogTool.modules.files_preperation import FilesPreperation

class TestRemoveTime(unittest.TestCase):
    """ Tests the function remove_time """

    def setUp(self):
        self._fp = FilesPreperation()

    @patch("builtins.input", side_effect=["0", "0"])
    def test_remove_time_0min_removed(self, mock_input):
        """ Tests if remove_time function works as intended by entering '0' in both remove_start and remove_end.
            This test needs the files 'expected_test_file.csv' and 'actual_original_test_file.csv' to work. """
        # csv file containing how the file should look like after using remove_time function.
        expected_file_path = r"SleepLogTool\test_folder\csv_test_files\expected_test_file_full_2min.csv"
        with open(expected_file_path, newline='') as csvfile:
            expected = [row for row in csv.DictReader(csvfile)]

        # csv file containing the file to be modified by remove_time function.
        actual_original_file_path = r"SleepLogTool\test_folder\csv_test_files\actual_original_test_file.csv"
        df = self._fp.csv_to_panda(actual_original_file_path)
        pd_df = pd.DataFrame(self._fp.remove_time(df))
        # csv file being saved after modified.
        actual_modified_file_path = r"SleepLogTool\test_folder\csv_test_files\actual_modified_test_file.csv"
        pd_df.to_csv(actual_modified_file_path, index=False, float_format="%.6f")

        with open(actual_modified_file_path, newline='') as csvfile:
            actual = [row for row in csv.DictReader(csvfile)]

        self.assertEqual(expected, actual)

    @patch("builtins.input", side_effect=["0.5", "0.5"])
    def test_remove_time_30sec_removed_start_and_end(self, mock_input):
        """ Tests if remove_time function works as intended by entering '0.5' in both remove_start and remove_end.
            This test needs the files 'expected_test_file.csv' and 'actual_original_test_file.csv' to work. """
        # csv file containing how the file should look like after using remove_time function.
        expected_file_path = r"SleepLogTool\test_folder\csv_test_files\expected_test_file_removed_0_5min_start_and_end.csv"
        with open(expected_file_path, newline='') as csvfile:
            expected = [row for row in csv.DictReader(csvfile)]

        # csv file containing the file to be modified by remove_time function.
        actual_original_file_path = r"SleepLogTool\test_folder\csv_test_files\actual_original_test_file.csv"
        df = self._fp.csv_to_panda(actual_original_file_path)
        pd_df = pd.DataFrame(self._fp.remove_time(df))
        # csv file being saved after modified.
        actual_modified_file_path = r"SleepLogTool\test_folder\csv_test_files\actual_modified_test_file.csv"
        pd_df.to_csv(actual_modified_file_path, index=False, float_format="%.6f")

        with open(actual_modified_file_path, newline='') as csvfile:
            actual = [row for row in csv.DictReader(csvfile)]

        self.assertEqual(expected, actual)

    def tearDown(self):
        self._fp = None
