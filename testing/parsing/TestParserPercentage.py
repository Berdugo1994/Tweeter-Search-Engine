import unittest
from parser_module import Parse


class TestParserPercentage(unittest.TestCase):
    def test_percentage1(self):
        text = "6%"
        expected = ["6%"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_percentage2(self):
        text = "10.6 percent"
        expected = ["10.6%"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_percentage3(self):
        text = "10.6 percentage"
        expected = ["10.6%"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_percentage4(self):
        text = "6.3%"
        expected = ["6.3%"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_percentage5(self):
        text = "6.30%"
        expected = ["6.3%"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_percentage6(self):
        text = "8,336%"
        expected = ["8336%"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_percentage7(self):
        text = "6 %"
        expected = ["6%"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_percentage8(self):
        text = "3.1k%"
        expected = ["3.1k%"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
