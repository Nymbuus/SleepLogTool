import unittest   # The test framework

class Test_TestIncrementDecrement(unittest.TestCase):
    def test_increment(self):
        self.assertEqual(4, 4)

    # This test is designed to fail for demonstration purposes.
    def test_decrement3(self):
        with self.assertRaises(AssertionError):
            self.assertEqual(3, 4)

    def test_decrement5(self):
        with self.assertRaises(AssertionError):
            self.assertEqual(5, 4)

if __name__ == '__main__':
    unittest.main()