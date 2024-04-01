import unittest
from unittest.mock import patch
from SleepLogTool.modules.files_preperation import FilesPreperation
import pandas as pd

class TestRemoveTime(unittest.TestCase):
    """ Test for remove_time function in files_preperation.py """

    def setUp(self):
        self._fp = FilesPreperation()
        self.df = self._fp.blf_to_df(["SleepLogTool\\blf_testfiles\\Trace_BP11_Display_1_20240221_133700_20240221_133859_#08-1_LEM.blf"])

    def test_remove_time_correct_return(self):
        """ Checks if the function returns a pandas dataframe. """
        self.assertEqual(type(self._fp.remove_time(self.df, 0.1, 0.1)), pd.core.frame.DataFrame)

    def test_remove_time_int_arguments(self):
        """ Checks if the function handles int arguments. """
        self.assertEqual(type(self._fp.remove_time(self.df, 1, 1)), pd.core.frame.DataFrame)

    def test_remove_time_string_first_argument(self):
        """ Checks if the function raises TypeError if first argument is a string. """
        with self.assertRaises(TypeError):
            self._fp.remove_time(self.df, 1, "_")

    def test_remove_time_string_second_argument(self):
        """ Checks if the function raises TypeError if second argument is a string. """
        with self.assertRaises(TypeError):
            self._fp.remove_time(self.df, "_", 1)
        
    def test_remove_time_correct_length_start_time_remove(self):
        """ Checks if df has correct length after calling function with 1min removed from start. """
        expected_length = 6012
        self.assertEqual(len(self._fp.remove_time(self.df, 6000, 0)), expected_length)

    def test_remove_time_correct_length_end_time_remove(self):
        """ Checks if df has correct length after calling function with 1min removed from end. """
        expected_length = 6012
        self.assertEqual(len(self._fp.remove_time(self.df, 0, 6000)), expected_length)

    def tearDown(self):
        self._fp = None

if __name__ == "__main__":
    unittest.main()