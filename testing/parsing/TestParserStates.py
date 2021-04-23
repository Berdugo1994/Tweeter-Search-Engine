import unittest
from parser_module import Parse


class TestParserStates(unittest.TestCase):

    def test_countries1(self):
        text = "USA"
        expected = ["USA"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_countries2(self):
        text = "U.S.A"
        expected = ["USA"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_countries3(self):
        text = "U_S_A"
        expected = ["USA"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_countries4(self):
        text = "U S A"
        expected = ["USA"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_countries5(self):
        text = "US"
        expected = ["USA"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_cities1(self):
        text = "new york"
        expected = ["NY"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_cities2(self):
        text = "NY"
        expected = ["NY"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_cities3(self):
        text = "ny"
        expected = ["NY"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_cities4(self):
        text = "US_NY"
        expected = ["NY"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_cities5(self):
        text = "New York"
        expected = ["NY"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_cities6(self):
        text = "New-York"
        expected = ["NY"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_cities7(self):
        text = "this is New York"
        expected = ["NY"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_cities8(self):
        text = "new york place good"
        expected = ["NY", "place", "good"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
