import unittest
from parser_module import Parse


class TestParserEmoji(unittest.TestCase):
    def test_emoji1(self):
        text = "I am so 😊"
        expected = ['smiling', 'face', 'with', 'smiling', 'eyes']
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_emoji2(self):
        text = "what is wrong with this world 😡"
        expected = ['wrong', 'world', 'pouting', 'face']
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_emoji3(self):
        text = "Want to eat 🍟🍕"
        expected = ['Want', 'eat', 'french', 'fries', 'pizza']
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_emoji4(self):
        text = "Want to eat🍟"
        expected = ['Want', 'eat', 'french', 'fries']
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
