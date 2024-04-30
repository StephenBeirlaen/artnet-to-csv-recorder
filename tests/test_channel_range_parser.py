import unittest

from channel_range_parser import ChannelRangeParser


class TestChannelRangeParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.channel_range_parser = ChannelRangeParser()

    def test_it_parses_single_value(self):
        channel_range_input = "1"
        expected = [1]
        actual = self.channel_range_parser.parse(channel_range_input)

        self.assertEqual(expected, actual)

    def test_it_parses_multiple_separate_values(self):
        channel_range_input = "1,2,5"
        expected = [1, 2, 5]
        actual = self.channel_range_parser.parse(channel_range_input)

        self.assertEqual(expected, actual)

    def test_it_parses_single_range(self):
        channel_range_input = "1-3"
        expected = [1, 2, 3]
        actual = self.channel_range_parser.parse(channel_range_input)

        self.assertEqual(expected, actual)

    def test_it_parses_multiple_ranges(self):
        channel_range_input = "2-4,6-8"
        expected = [2, 3, 4, 6, 7, 8]
        actual = self.channel_range_parser.parse(channel_range_input)

        self.assertEqual(expected, actual)

    def test_it_parses_more_ranges(self):
        channel_range_input = "2-4,6-8,100-101"
        expected = [2, 3, 4, 6, 7, 8, 100, 101]
        actual = self.channel_range_parser.parse(channel_range_input)

        self.assertEqual(expected, actual)

    def test_it_ignores_input_order(self):
        channel_range_input = "100-101,6-8,2-4"
        expected = [2, 3, 4, 6, 7, 8, 100, 101]
        actual = self.channel_range_parser.parse(channel_range_input)

        self.assertEqual(expected, actual)

    def test_it_removes_duplicates(self):
        channel_range_input = "2-4,2,3,4"
        expected = [2, 3, 4]
        actual = self.channel_range_parser.parse(channel_range_input)

        self.assertEqual(expected, actual)

    @unittest.expectedFailure
    def test_it_fails_on_empty_input(self):
        channel_range_input = ""
        self.channel_range_parser.parse(channel_range_input)
