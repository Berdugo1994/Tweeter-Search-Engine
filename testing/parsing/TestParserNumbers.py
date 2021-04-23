import unittest

from parser_module import Parse


class TestParserNumbers(unittest.TestCase):

    def test_numbers_under_thousand1(self):
        text = "204"
        expected = ["204"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_under_thousand2(self):
        text = "35.66"
        expected = ["35.66"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_fraction(self):
        text = "35 3/4"
        expected = ["35 3/4"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_fraction2(self):
        text = "35 3/4.5"
        expected = ["35 3/4.5"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_fraction2(self):
        text = "35 3/4/5/6"
        expected = ["35 3/4", "5/6"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_thousand1(self):
        text = "10,123"
        expected = ["10.123K"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_thousand2(self):
        text = "123 Thousand"
        expected = ["123K"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_thousand3(self):
        text = "1010.56"
        expected = ["1.01K"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_thousand4(self):
        text = "1.23 thousands"
        expected = ["1.23K"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_thousand5(self):
        text = "1000"
        expected = ["1K"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_with_k_lower(self):
        text = "10k"
        expected = ["10K"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_with_k_lower_and_more_words(self):
        text = "10k word"
        expected = ["10K", "word"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_with_k_upper(self):
        text = "10K"
        expected = ["10K"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_million1(self):
        text = "10,123,000"
        expected = ["10.123M"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_million11(self):
        text = "10,123,456"
        expected = ["10.123M"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_million2(self):
        text = "55 Million"
        expected = ["55M"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_millions(self):
        text = "55 Millions"
        expected = ["55M"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_millions1(self):
        text = "55 millions"
        expected = ["55M"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_millions2(self):
        text = "55 MILLIONS"
        expected = ["55M"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_millions3(self):
        text = "1000000"
        expected = ["1M"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_with_word(self):
        text = "55 people"
        expected = ["55", "people"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_with_m_lower(self):
        text = "55m"
        expected = ["55M"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_with_m_upper(self):
        text = "55M"
        expected = ["55M"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_Billion1(self):
        text = "10,123,000,000"
        expected = ["10.123B"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_Billion2(self):
        text = "55 Billion"
        expected = ["55B"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_Billion3(self):
        text = "1000000000"
        expected = ["1B"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_Billion_last(self):
        text = "the number is 5400000000 very big"
        expected = ["number", "5.4B", "big"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_Billion_last1(self):
        text = "the number is 1000000001 very big"
        expected = ["number", "1B", "big"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_Billion_last2(self):
        text = "the number is 1000000010 very big"
        expected = ["number", "1B", "big"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_k(self):
        text = "10.6k"
        expected = ["10.6K"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_k_comma(self):
        text = "60,000"
        expected = ["60K"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_numbers_over_k_sentence(self):
        text = "you're now at 60,000 cases per day"
        expected = ["60K", "cases", "per", "day"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_number_with_word(self):
        text = "19Outbreak"
        expected = ["19Outbreak"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_number_with_word2(self):
        text = "19 Outbreak"
        expected = ["19", "Outbreak"]
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_ip(self):
        text = '0.220.050.181.00'
        expected = ['0.220', '050.181', '00']
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_text_with_fractions(self):
        text = 'Ratios of means per phase-change: 0.22, 0.05, 0.18, 1.00. 3/'
        expected = ['Ratios', 'means', 'per', 'phase-change', '0.22', '0.05', '0.18', '1.00', '3']
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_number_with_sign_and_more_digits(self):
        text = '16M2'
        expected = ['16M2']
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_number_with_sign_and_more_digits2(self):
        text = '16M,2'
        expected = ['16M', '2']
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_number_break_lines(self):
        text = '1.  #USA - 1.63M\n' + \
               '2.  #Brazil - 530K\n' + \
               '3.  #India - 271K\n' + \
               '4.  #Russia - 218K\n' + \
               '5.  #SouthAfrica - 114K\n'
        expected = ['1', '#usa', 'usa', '1.63M', '2', '#brazil', 'brazil', '530K', '3', '#india', 'india', '271K', '4',
                    '#russia', 'russia', '218K', '5', '#southafrica', 'south', 'africa', '114K']
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    # def test_unicode_number(self):
    #     text = '½'
    #     expected = ['0.5']
    #     actual = Parse().parse_sentence(text)
    #
    #     self.assertEqual(expected, actual)

    def test_number_minus(self):
        text = 'Trump’s policy concerning COVID-19, which has already killed 130K and is still killing 500 -1,000 ppl a day'
        expected = ['Trump', 'policy', 'concerning', 'COVID19', '19', 'already', 'killed',
                    '130K', 'still', 'killing', '500', '-1000', 'ppl', 'day']
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_number_plus(self):
        text = '3,076,066\n+48,598 Active cases'
        expected = ['3.076M', '48.598K', 'Active', 'cases']
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_number_dots(self):
        text = '25,300.12'
        expected = ['25.3K', '12']
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_number_dots_with_space(self):
        text = '25,300. 12'
        expected = ['25.3K', '12']
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_number_dots2(self):
        text = '403,175  32,408  19.4 50,300'
        expected = ['403.175K', '32.408K', '19.4', '50.3K']
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)

    def test_failing(self):
        text = 'Being from the US right now is literally an embarrassment https://t.co/6ypNr91AS0'
        expected = ['https', 't.co', '6ypNr91AS0', 'USA', 'right', 'literally', 'embarrassment']
        actual = Parse().parse_sentence(text)

        self.assertEqual(expected, actual)
