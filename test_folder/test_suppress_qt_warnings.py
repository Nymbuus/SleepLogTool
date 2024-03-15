""" Imports. """
import unittest
from sleep_log_tool_repo.sleep_log_tool import SleepLogTool


class TestSleepLogTool(unittest.TestCase):
    """ suppress_qt_warnings in sleep_log_tool.py """

    # def setUp(self):
    #     self._sleeplogtool = SleepLogTool()

    def test_suppress_qt_warnings_success(self):
        """ Test if function returns True. """
        self.assertEqual(SleepLogTool.suppress_qt_warnings(self), True)

    def test_suppress_qt_warnings_fail(self):
        """ Test if function returns False. """
        self.assertEqual(SleepLogTool.suppress_qt_warnings(self), False)

    def test_suppress_qt_warnings_fail2(self):
        """ Test if function returns False. """
        self.assertEqual(SleepLogTool.suppress_qt_warnings(self), False)

    # def tearDown(self):
    #     self._sleeplogtool = None


if __name__ == '__main__':
    unittest.main()
