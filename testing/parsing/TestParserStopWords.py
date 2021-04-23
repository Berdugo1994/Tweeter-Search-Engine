import unittest
from parser_module import Parse


class TestParserStopWords(unittest.TestCase):

    def test_stopword_upper(self):
        text = "he is funny"
        expected = ["funny"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_stopword_lower(self):
        text = "He Is Funny"
        expected = ["funny"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_stopword_special_char(self):
        text = "He's Funny"
        expected = ["funny"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
