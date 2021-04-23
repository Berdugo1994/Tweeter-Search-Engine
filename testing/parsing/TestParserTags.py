import unittest
from parser_module import Parse


class TestParserTags(unittest.TestCase):

    def test_tag(self):
        text = "@sarit"
        expected = ["@sarit"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_tag2(self):
        text = "@saritHollander"
        expected = ["@saritHollander"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_tag3(self):
        text = "@sarit_hollander"
        expected = ["@sarit_hollander"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
