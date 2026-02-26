import os
import sys
import unittest

# make sure project modules importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.files_preperation import FilesPreparation

class DummyMsg:
    def __init__(self, channel, arbitration_id, timestamp, data):
        self.channel = channel
        self.arbitration_id = arbitration_id
        self.timestamp = timestamp
        self.data = data


class TestConcatenationOffsets(unittest.TestCase):
    def setUp(self):
        self.fp = FilesPreparation(show_warning_func=lambda m: None, plot_line_frames=[])
        # stub methods
        self.fp.get_attribute = lambda f,a: 0 if a=='start_timestamp' else 3

    def test_lem_blf_offset(self):
        # first file channel 10, second file channel 10
        def fake_yield(file):
            if file=='f1.blf':
                return iter([DummyMsg(10,None,1,[0,0,0,0]), DummyMsg(10,None,2,[0,0,0,0]), DummyMsg(10,None,3,[0,0,0,0])])
            if file=='f2.blf':
                return iter([DummyMsg(10,None,1,[0,0,0,0]), DummyMsg(10,None,2,[0,0,0,0])])
            return iter([])
        self.fp.yield_message = fake_yield
        dfs = self.fp.convert_to_df(['f1.blf','f2.blf'], lem_graph=True, bl_graph=False, invert_lem=False)
        times = dfs[0]['df']['Time'].tolist()
        self.assertEqual(times, [0,1,2,3,4,5])

    def test_bus_blf_offset(self):
        def fake_yield(file):
            # only busload channel
            if file=='a.blf':
                return iter([DummyMsg(2,None,1,[0,0,0,0]), DummyMsg(2,None,2,[0,0,0,0])])
            if file=='b.blf':
                return iter([DummyMsg(2,None,1,[0,0,0,0]), DummyMsg(2,None,2,[0,0,0,0])])
            return iter([])
        self.fp.yield_message = fake_yield
        dfs = self.fp.convert_to_df(['a.blf','b.blf'], lem_graph=False, bl_graph=True, invert_lem=False)
        # find the blf entry and look at timestamps
        times = dfs[0]['df']['Time'].tolist()
        # each file contributed four seconds worth of points so there should be 8
        self.assertEqual(times, list(range(8)))

    def tearDown(self):
        self.fp = None

if __name__ == '__main__':
    unittest.main()
