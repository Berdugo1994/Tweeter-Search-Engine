import string

from nltk import TweetTokenizer, PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from document import Document
from parsers import UrlParser, EmojiParser, HashtagParser, NumbersParser
from parsers.Covid19Parser import Covid19Parser
from parsers.SubdivisionParser import SubdivisionParser


class Parse:

    def __init__(self, should_stem=False):
        self.tokenizer = TweetTokenizer()
        single_chars = list(string.printable.replace("0123456789", ""))
        self.stop_words = frozenset(stopwords.words('english'))
        internal_stop_words = ['..', '.', '—', '️', '...', '”', '“', '…', '‘', '', 'he\'s', 'she\'s', 'rt',
                               'tl;dr', 'you\'re', 'i\'m', 'you\'ll', 'i\'ll',
                               'she\'ll', 'https', 'http', 't.co', 'he\'ll', '’'] + \
                              single_chars
        self.stop_words = set(list(self.stop_words) + internal_stop_words)
        self.subdivisionParser = SubdivisionParser()
        self.covid19Parser = Covid19Parser()
        self.porter = PorterStemmer()
        self.should_stem = should_stem

    def parse_sentence(self, original_text, stop_word=True):
        """
        This function tokenize, remove stop words and apply lower case for every word within the text
        :param original_text: the text to parse
        :param stop_word: boolean param. will be false when most of the world is stop words
        :return: the text as tokens
        """
        text = original_text
        text_tokens_without_stopwords = []

        url_result = UrlParser.url_func(text)
        url_exist = url_result[0]
        if url_exist:
            if url_result[1]:
                self.stop_words.update(url_result[1])
            # text_tokens_without_stopwords += url_result[1]
            text = url_result[2]

        text_tokens = self.tokenizer.tokenize(text)
        num_of_words = len(text_tokens)
        i = 0
        while i < num_of_words:
            word = text_tokens[i]
            lower_word = word.lower()
            is_find, i, translated_word = self.subdivisionParser.parse_word(lower_word, i, text_tokens)
            if is_find:
                text_tokens_without_stopwords.append(translated_word)
                i = i + 1
                continue

            if self.is_stop_word(lower_word) and stop_word:
                i = i + 1
                continue

            is_find, i, translated_word = self.covid19Parser.parse_word(lower_word, i, text_tokens)

            if is_find:
                text_tokens_without_stopwords.append(translated_word)
                i = i + 1
                continue

            if word[0].islower():
                if self.should_stem:
                    word = self.porter.stem(word)
                if stop_word:
                    self.add_to_terms(text_tokens_without_stopwords, word, lower_word)
                else:
                    text_tokens_without_stopwords.append(word)
                i = i + 1
                continue

            emoji_parser_result = EmojiParser.parse_word(word)
            # translate emojies to list of words
            if emoji_parser_result[0]:
                text_tokens_without_stopwords += emoji_parser_result[1]
                i = i + 1
                continue

            if word[0] == '#':
                word = text_tokens[i]
                new_words, num_of_words_in_hashtag = HashtagParser.parse_hashtag(word)
                text_tokens_without_stopwords += new_words
            elif word[0] == '@':
                text_tokens_without_stopwords.append(word)
            elif NumbersParser.is_number(word):
                word, i = NumbersParser.collect_trailing_number(i, text_tokens, word, text)
                if i < num_of_words - 1:
                    next_word = text_tokens[i + 1]
                    next_word_lower = next_word.lower()
                    if NumbersParser.is_percentage(next_word_lower):
                        text_tokens_without_stopwords.append(NumbersParser.to_numeric(word) + '%')
                        i += 1
                    elif NumbersParser.is_number_notation(next_word_lower):
                        text_tokens_without_stopwords.append(word + NumbersParser.kmb_sign(next_word_lower))
                        i += 1
                    elif NumbersParser.is_fraction(next_word):
                        text_tokens_without_stopwords.append(word + " " + next_word)
                        i += 1
                    else:
                        text_tokens_without_stopwords.append(NumbersParser.normalize_number(word))
                else:
                    text_tokens_without_stopwords.append(NumbersParser.normalize_number(word))
            elif NumbersParser.is_number_with_notation(word):
                text_tokens_without_stopwords.append(word.upper())
            # Here will be only upper case word - append as they are
            else:
                text_tokens_without_stopwords.append(word)
            i += 1
        # in case of all of the word is built of stop words, will not be recursion because of stop_word param.
        if len(text_tokens_without_stopwords) == 0 and stop_word:
            return self.parse_sentence(original_text, stop_word=False)
        return text_tokens_without_stopwords

    def parse_doc(self, doc_as_list):
        """
        This function takes a tweet document as list and break it into different fields
        :param doc_as_list: list re-presenting the tweet.
        :return: Document object with corresponding fields.
        """
        tweet_id = doc_as_list[0]
        tweet_date = doc_as_list[1]
        full_text = doc_as_list[2]
        url = doc_as_list[3]
        retweet_text = doc_as_list[4]
        retweet_url = doc_as_list[5]
        quote_text = doc_as_list[6]
        quote_url = doc_as_list[7]

        term_dict = {}
        tokenized_text = self.parse_sentence(full_text)

        doc_length = len(tokenized_text)  # after text operations.

        # Counts for every term number of mentions in the tweet.
        for term in tokenized_text:
            if term not in term_dict.keys():
                term_dict[term] = 1
            else:
                term_dict[term] += 1

        document = Document(tweet_id, tweet_date, full_text, url, retweet_text, retweet_url, quote_text,
                            quote_url, term_dict, doc_length)
        return document

    def is_stop_word(self, lower_word):
        return lower_word in self.stop_words

    def add_to_terms(self, text_tokens_without_stopwords, word, lower_word):
        if not self.is_stop_word(lower_word):
            text_tokens_without_stopwords.append(word)
