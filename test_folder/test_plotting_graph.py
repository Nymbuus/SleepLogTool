import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sleep_log_tool_repo.sleep_log_tool import SleepLogTool

class TestPlottingGraph(unittest.TestCase):
    """ Tests plotting_graph function in sleep_log_tool """

    def setUp(self):
        self._slt = SleepLogTool()

    @patch('matplotlib.pyplot.plot')
    @patch('matplotlib.pyplot.xlabel')
    @patch('matplotlib.pyplot.ylabel')
    @patch('matplotlib.pyplot.title')
    @patch('matplotlib.pyplot.subplots_adjust')
    @patch('matplotlib.pyplot.grid')
    @patch('matplotlib.pyplot.get_current_fig_manager')
    @patch('matplotlib.pyplot.show')
    def test_plotting_graph(self, mock_show, mock_get_current_fig_manager, mock_grid, mock_subplots_adjust,
                            mock_title, mock_ylabel, mock_xlabel, mock_plot):
        # Mock DataFrame.
        df = pd.DataFrame({'Time': [0, 1, 2, 3, 4], 'Current': [10, 20, 30, 40, 50]})
        self._slt.plotting_graph(df)

        # Assert calls to pyplot functions with correct arguments.
        y = df["Current"].to_numpy()
        x = df["Time"].to_numpy()
        mock_xlabel.assert_called_once_with("Time(h)", fontsize=15)
        mock_ylabel.assert_called_once_with("Current(mA)", fontsize=15)
        mock_title.assert_called_once_with("Sleeplog analysis", fontsize=24)
        mock_subplots_adjust.assert_called_once_with(left=0.05, bottom=0.06, right=0.97, top=0.955,
                                                     wspace=None, hspace=None)
        mock_grid.assert_called_once()
        mock_get_current_fig_manager.assert_called_once()
        mock_show.assert_called_once()

if __name__ == '__main__':
    unittest.main()