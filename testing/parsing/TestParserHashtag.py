import unittest
from parser_module import Parse


class test_ParserHashtag(unittest.TestCase):

    def test_hashtags1(self):
        # Test 1
        text = "#stayAtHome"
        expected = ["stay", "at", "home", "#stayathome"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(sorted(expected), sorted(actual))

    def test_hashtags2(self):
        # Test 2
        text = "#stay_at_home"
        expected = ["stay", "at", "home", "#stayathome"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(sorted(expected), sorted(actual))

    def test_hashtags3(self):
        # Test 3
        text = "#stay_at_home Eden Berdugo"
        expected = {"stay", "at", "home", "#stayathome", "Eden", "Berdugo"}
        actual = Parse().parse_sentence(text)
        self.assertEqual(sorted(expected), sorted(actual))

    def test_hashtags4(self):
        # Test 1
        text = "#at"
        expected = ["at", "#at"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(sorted(expected), sorted(actual))

    def test_hashtags5(self):
        # Test 1
        text = "#EdenBerdugo eat"
        expected = ["eden", "berdugo", "#edenberdugo", "eat"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(sorted(expected), sorted(actual))

    def test_hashtags6(self):
        # Test 1
        text = "#at"
        expected = ["at", "#at"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(sorted(expected), sorted(actual))

    def test_hashtags7(self):
        text = "#CULTforGOOD eden"
        expected = ["cult", "for", "good", "#cultforgood", "eden"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(sorted(expected), sorted(actual))

    def test_hashtags7(self):
        text = "#CULTforGOODd eden"
        expected = ["cult", "for", "good", "d", "#cultforgoodd", "eden"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(sorted(expected), sorted(actual))

    def test_hashtags8(self):
        text = "#NOs4Ever eden"
        expected = ["no", "s", "4", "ever", "#nos4ever", "eden"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(sorted(expected), sorted(actual))


    def test_hashtags8(self):
        text = "#stayathome"
        expected = ["#stayathome", "stayathome"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(sorted(expected), sorted(actual))

    def test_hashtags9(self):
        text = "#COVID19"
        expected = ['#covid19', 'covid', '1', '9']
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
