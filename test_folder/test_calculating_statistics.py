import unittest
import pandas as pd
from io import StringIO
import sys
from sleep_log_tool_repo.sleep_log_tool import SleepLogTool

class TestCalculatingStatistics(unittest.TestCase):
    """ Tests calculating_statistics in sleep_log_tool """

    def setUp(self):
        self._slt = SleepLogTool()

    def test_calculating_statistics(self):
        # Create a DataFrame with test data
        data = {
            'Current': [10, 20, 30, 40, 50],
            'Time': [0, 1000, 2000, 3000, 4000]
        }
        df = pd.DataFrame(data)

        self._slt.calculating_statistics(df)

        # Redirect stdout to capture print statements
        captured_output = StringIO()
        sys.stdout = captured_output

        # Call the method being tested
        self._slt.calculating_statistics(df)

        # Reset redirect
        sys.stdout = sys.__stdout__

        # Get the printed output
        captured_output = captured_output.getvalue()

        # Check if the output contains the expected strings
        self.assertIn("Average Current: 30.000mA", captured_output)
        self.assertIn("Max Current: 50 mA", captured_output)
        self.assertIn("Min Current: 10 mA", captured_output)
        self.assertIn("Total time: 1.111 hours or 66.7 minutes.", captured_output)
        self.assertIn("Ampere hours: 0.0333 Ah", captured_output)

if __name__ == "__main__":
    unittest.main()
