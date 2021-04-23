import unittest
from parser_module import Parse


class testParserCovid(unittest.TestCase):
    def test_covid1(self):
        # Test 1d
        text = "covid-19"
        expected = ["COVID19", "19"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_covid2(self):
        # Test 1
        text = "#stayAtHome covid19"
        expected = ["#stayathome", "stay", "at", "home", "COVID19", "19"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_covid3(self):
        # Test 1
        text = "#stayAtHome COVID-19"
        expected = ["#stayathome", "stay", "at", "home", "COVID19", "19"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_covid4(self):
        # Test 1
        text = "#stayAtHome Covid"
        expected = ["#stayathome", "stay", "at", "home", "COVID19"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_covid5(self):
        # Test 1
        text = "#stayAtHome COVID19"
        expected = ["#stayathome", "stay", "at", "home", "COVID19", "19"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_covid6(self):
        # Test 1
        text = "corona virus #stayAtHome covid"
        expected = ['COVID19', '#stayathome', 'stay', 'at', 'home', 'COVID19']
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_covid7(self):
        text = "covid19"
        expected = ["COVID19", "19"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_covid8(self):
        text = "coVid19"
        expected = ["COVID19", "19"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_covid8(self):
        text = "COVID19"
        expected = ["COVID19", "19"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)

    def test_covid9(self):
        text = "ovid"
        expected = ["COVID19"]
        actual = Parse().parse_sentence(text)
        self.assertEqual(expected, actual)
