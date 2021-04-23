class Covid19Parser:
    def __init__(self):
        self.covid19Translated = "COVID19"

        self.multi_words_dict = {
            "corona": [(['corona', 'virus'], self.covid19Translated)],
            "covid": [(['covid', '19'], self.covid19Translated)],
        }

        self.corona_dict = {
            "covid-19": self.covid19Translated,
            "covid": self.covid19Translated,
            "coronavirus": self.covid19Translated
        }

    def parse_word(self, lower_word, current_index, words):
        if lower_word in self.corona_dict:
            return True, current_index, self.corona_dict[lower_word]

        if lower_word in self.multi_words_dict:
            words = [word.lower() for word in words]
            for tuple in self.multi_words_dict[lower_word]:
                if tuple[0] == words[current_index:current_index + len(tuple[0])]:
                    return True, current_index + len(tuple[0]) - 1, tuple[1]
        return False, current_index, None
