import json
import os
from os.path import dirname


class SubdivisionParser:
    def __init__(self):
        json = self._get_json()

        temp_multi_words_dict = {
            "united states": "US",
            "us of america": "USA",
            "u s a": "USA",
            "u . s . a": "USA",
        }
        # self.sorted_multi_keys = sorted(self.multi_words_dict.keys())
        # self.sorted_single_keys = sorted(self.divisions_dict.keys())
        self.divisions_dict = {
            "usa": "USA",
            "u_s_a": "USA",
            "u-s-a": "USA"
        }

        for key in json:
            country = key.split('-')[0]
            state = key.split('-')[1]
            lower_state = state.lower()
            full_name = json[key].lower()
            self.divisions_dict[key.lower()] = state
            self.divisions_dict[country.lower() + '_' + lower_state] = state

            if ' ' in full_name:
                temp_multi_words_dict[full_name] = state
                self.divisions_dict[full_name.replace(' ', '-')] = state
            else:
                self.divisions_dict[full_name] = state

        self.multi_words_dict = {}

        for k in temp_multi_words_dict.keys():
            value = temp_multi_words_dict[k]
            splitted = k.split(' ')
            first_word = splitted[0]
            if first_word not in self.multi_words_dict:
                self.multi_words_dict[first_word] = []
            self.multi_words_dict[splitted[0]].append((splitted, value))

    def _get_json(self):

        path = r'resources/parser/subdivisions_US.json'

        with open(path) as f:
            return json.load(f)

    def parse_word(self, lower_word, current_index, words):
        if lower_word in self.divisions_dict:
            return True, current_index, self.divisions_dict[lower_word]

        if lower_word in self.multi_words_dict:
            words = [word.lower() for word in words]
            for tuple in self.multi_words_dict[lower_word]:
                if tuple[0] == words[current_index:current_index + len(tuple[0])]:
                    return True, current_index + len(tuple[0]) - 1, tuple[1]
        return False, current_index, None
