""" Imports. """
import unittest
from sleep_log_tool.sleep_log_tool import SleepLogTool


class TestSleeplogtool(unittest.TestCase):
    """ Tests sleep_log_tool.py """

    def setUp(self):
        self._sleeplogtool = SleepLogTool()

    def test_fail(self):
        """ Test fail """
        self.assertIsNone(1)

    def test_success(self):
        """ Test success. """
        self.assertEqual(1, 1)

    def test_suppress_qt_warnings(self):
        """ Test if function returns True. """
        self.assertEqual(self._sleeplogtool.suppress_qt_warnings(), True)

    def tearDown(self):
        self._sleeplogtool = None


if __name__ == '__main__':
    unittest.main()
