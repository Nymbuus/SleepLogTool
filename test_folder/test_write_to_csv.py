import os
import unittest
from unittest.mock import patch
from sleep_log_tool_repo.sleep_log_tool import SleepLogTool
import csv

class TestWriteToCsv(unittest.TestCase):
    """ Tests the write_to_csv function in sleep_log_tool. """

    def setUp(self):
        self._slt = SleepLogTool()
    
    def test_write_to_csv_correct_values(self):
        """ Tests if the function returns a csv file with correct values. """
        actual_file_path = "SleepLogTool\\test_folder\\csv_test_files\\actual_write_to_csv_test_file.csv"
        
        # writes Time and Current at the top of the file since it's not done in this function.
        # It's needed for simulating how it would be done in a real situation.
        out = ["Time", "Current"]
        with open(actual_file_path, 'w', encoding='UTF8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=out)
            writer.writeheader()

        actual_file_path = self._slt.write_to_csv(actual_file_path, ["SleepLogTool\\blf_testfiles\\Trace_BP11_Display_1_20240221_133700_20240221_133859_#08-1_LEM.blf"])
        with open(actual_file_path, newline='') as csvfile:
            actual_result = [row for row in csv.DictReader(csvfile)]
        os.remove(actual_file_path)
        
        expected_file_path = "SleepLogTool\\test_folder\\csv_test_files\\expected_write_to_csv_test_file.csv"
        with open(expected_file_path, newline='') as csvfile:
            expected_result = [row for row in csv.DictReader(csvfile)]

        self.assertEqual(actual_result, expected_result)

    def test_write_to_csv_txt_in_file_name(self):
        """ Tests if the function will not accept .txt files. """
        file_path = "SleepLogTool\\blf_testfiles\\write_to_csv_test_txt.txt"
        f = open(file_path, "x")
        f.close()
        with self.assertRaises(TypeError):
            self._slt.write_to_csv(file_path, ["SleepLogTool\\blf_testfiles\\Trace_BP11_Display_1_20240221_133700_20240221_133859_#08-1_LEM.blf"])
        os.remove(file_path)

    def test_write_to_csv_txt_in_file_list(self):
        """ Tests if the function will not accept .txt files. """
        file_path = "SleepLogTool\\blf_testfiles\\write_to_csv_test_txt.txt"
        f = open(file_path, "x")
        f.close()
        with self.assertRaises(TypeError):
            self._slt.write_to_csv("SleepLogTool\\test_folder\\csv_test_files\\expected_write_to_csv_test_file.csv", file_path)
        os.remove(file_path)

    def tearDown(self):
        self._slt = None