import os
import unittest
import pandas as pd
from SleepLogTool.modules.files_preperation import FilesPreperation

class TestBlfToPd(unittest.TestCase):
    """ Tests the csv_to_panda function in sleep_log_tool. """

    def setUp(self):
        self._fp = FilesPreperation()
        blf_file = []
        blf_file.append("SleepLogTool\\blf_testfiles\\Trace_BP11_Display_1_20240221_133700_20240221_133859_#08-1_LEM.blf")
        self.df = self._fp.blf_to_df(blf_file)

    def test_blf_to_pd_correct_columns(self):
        """ Tests if the amount of columns is correct. """
        expected_columns_amount = 2
        self.assertListEqual(list(self.df.columns), ["Time", "Current"])
        self.assertEqual(len(self.df.columns), expected_columns_amount)

    def test_blf_to_pd_correct_rows(self):
        """ Tests if the amount of rows is correct. """
        expected_rows_amount = 12012
        self.assertEqual(len(self.df), expected_rows_amount)
    
    def test_blf_to_pd_correct_return(self):
        """ Tests if the return type is a pandas dataframe. """
        self.assertIsInstance(self.df, pd.DataFrame)

    def test_blf_to_pd_txt_file_input(self):
        """ Tests if the function will raise TypeError if the argument is anything other then a blf file. """
        f = open("blf_to_pd_txt_file_test.txt", "w")
        f.close()
        with self.assertRaises(TypeError):
            temp = self._fp.blf_to_df("blf_to_pd_txt_file_test.txt")
        os.remove("blf_to_pd_txt_file_test.txt")

    def tearDown(self):
        self._fp = None
