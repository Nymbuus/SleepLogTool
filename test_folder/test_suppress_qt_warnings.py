""" Imports. """
import unittest
from sleep_log_tool_repo.sleep_log_tool import SleepLogTool


class TestSleepLogTool(unittest.TestCase):
    """ Test for suppress_qt_warnings in sleep_log_tool.py """

    def setUp(self):
        self._sleeplogtool = SleepLogTool()

    def test_suppress_qt_warnings_success(self):
        """ Test if function returns True. """
        self.assertEqual(self._sleeplogtool.suppress_qt_warnings(), True)

    def test_suppress_qt_warnings_fail(self):
        """ Test if function returns False. """
        with self.assertRaises(AssertionError):
            self.assertEqual(self._sleeplogtool.suppress_qt_warnings(), False)

    def tearDown(self):
        self._sleeplogtool = None


if __name__ == '__main__':
    unittest.main()
