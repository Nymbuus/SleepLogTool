import os
import unittest
import pandas as pd
from SleepLogTool.modules.files_preperation import FilesPreperation

class TestCsvToPanda(unittest.TestCase):
    """ Tests the csv_to_panda function in sleep_log_tool. """

    def setUp(self):
        self._fp = FilesPreperation()
        self.df = self._fp.csv_to_panda("SleepLogTool\\test_folder\\csv_test_files\\actual_original_test_file.csv")

    def test_csv_to_panda_correct_columns(self):
        """ Tests if the amount of columns is correct. """
        expected_columns_amount = 2
        self.assertListEqual(list(self.df.columns), ["Time", "Current"])
        self.assertEqual(len(self.df.columns), expected_columns_amount)

    def test_csv_to_panda_correct_rows(self):
        """ Tests if the amount of rows is correct. """
        expected_rows_amount = 12012
        self.assertEqual(len(self.df), expected_rows_amount)
    
    def test_csv_to_panda_correct_return(self):
        """ Tests if the return type is a pandas dataframe. """
        self.assertIsInstance(self.df, pd.DataFrame)

    def test_csv_to_panda_txt_file_input(self):
        """ Tests if the function will raise TypeError if the argument is anything other a csv file. """
        f = open("csv_to_panda_txt_file_test.txt", "x")
        f.close()
        with self.assertRaises(TypeError):
            temp = self._fp.csv_to_panda("csv_to_panda_txt_file_test.txt")
        os.remove("csv_to_panda_txt_file_test.txt")

    def tearDown(self):
        self._fp = None
