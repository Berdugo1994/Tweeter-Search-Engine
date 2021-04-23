import unittest
import os
from module_glove import GloVe
from document import Document
from indexer import Indexer
from parser_module import Parse


class TestIndexerCases(unittest.TestCase):
    glove = GloVe()
    root = os.path.dirname(os.path.abspath(__file__))
    corpus_path = root + '\\corpus'
    output_path = root + '\\results_old'
    def test_upper_case(self):
        indexer = Indexer(self.glove,self.output_path)
        dict = {"Hello": 1, "goodbye": 1}
        doc = Document("tweet_id", "tweet_date", "full_text", "url", "retweet_text", "retweet_url", "quote_text",
                       "quote_url", dict, "doc_length")

        indexer.add_new_doc(doc)
        expected = {"HELLO", "goodbye"}
        actual = set(indexer.inverted_idx.keys())

        self.assertEqual(expected, actual)

    def test_upper_case2(self):
        indexer = Indexer(self.glove,self.output_path)
        dict = {"Hello": 1, "goodbye": 1}
        doc = Document("tweet_id", "tweet_date", "full_text", "url", "retweet_text", "retweet_url", "quote_text",
                       "quote_url", dict, "doc_length")

        indexer.add_new_doc(doc)
        dict = {"hello": 1, "Goodbye": 1}
        doc = Document("tweet_id2", "tweet_date", "full_text", "url", "retweet_text", "retweet_url", "quote_text",
                       "quote_url", dict, "doc_length")

        indexer.add_new_doc(doc)
        expected = {"hello", "goodbye"}
        actual = set(indexer.inverted_idx.keys())

        self.assertEqual(expected, actual)

    def test_upper_case3(self):
        indexer = Indexer(self.glove,self.output_path)
        dict = {"heLLo": 1, "Goodbye": 1}
        doc = Document("tweet_id", "tweet_date", "full_text", "url", "retweet_text", "retweet_url", "quote_text",
                       "quote_url", dict, "doc_length")

        indexer.add_new_doc(doc)
        expected = {"hello", "GOODBYE"}
        actual = set(indexer.inverted_idx.keys())

        self.assertEqual(expected, actual)

    def test_upper_case4(self):
        indexer = Indexer(self.glove,self.output_path)
        dict = {"heLLo": 1, "Goodbye": 1}
        doc = Document("tweet_id", "tweet_date", "full_text", "url", "retweet_text", "retweet_url", "quote_text",
                       "quote_url", dict, "doc_length")
        indexer.add_new_doc(doc)

        dict = {"HeLLo": 1, "GOODBYE": 1}
        doc = Document("tweet_id2", "tweet_date", "full_text", "url", "retweet_text", "retweet_url", "quote_text",
                       "quote_url", dict, "doc_length")

        indexer.add_new_doc(doc)
        expected = {"hello", "GOODBYE"}
        actual = set(indexer.inverted_idx.keys())

        self.assertEqual(expected, actual)

    def test_upper_case_file_saved(self):
        indexer = Indexer(self.glove,self.output_path)
        dict = {"Hello": 1, "goodbye": 1}
        doc = Document("tweet_id", "tweet_date", "full_text", "url", "retweet_text", "retweet_url", "quote_text",
                       "quote_url", dict, "doc_length")

        indexer.add_new_doc(doc)

        indexer.save_partial_indexer()

        dict = {"hello": 1, "Goodbye": 1}
        doc = Document("tweet_id2", "tweet_date", "full_text", "url", "retweet_text", "retweet_url", "quote_text",
                       "quote_url", dict, "doc_length")

        indexer.add_new_doc(doc)
        indexer.save_partial_indexer()
        indexer._do_upper_case_fixes()
        expected = {"hello", "goodbye"}
        actual = set(indexer.inverted_idx.keys())

        self.assertEqual(expected, actual)

    def test_upper_case2_save_file(self):
        indexer = Indexer(self.glove,self.output_path)
        dict = {"heLLo": 1, "Goodbye": 1}
        doc = Document("tweet_id", "tweet_date", "full_text2", "url", "retweet_text", "retweet_url", "quote_text",
                       "quote_url", dict, "doc_length")
        indexer.add_new_doc(doc)

        indexer.save_partial_indexer()

        dict = {"HeLLo": 1, "GOODBYE": 1}
        doc = Document("tweet_id2", "tweet_date", "full_text", "url", "retweet_text", "retweet_url", "quote_text",
                       "quote_url", dict, "doc_length")

        indexer.add_new_doc(doc)
        expected = {"hello", "GOODBYE"}
        actual = set(indexer.inverted_idx.keys())

        self.assertEqual(expected, actual)

    def test_upper_case_failing(self):
        text = 'cat and jack kids face mask 2 packs 4  Cat and Jack Kids Face Mask'
        p = Parse().parse_sentence(text)
        indexer = Indexer(GloVe(), 'C:\\Users\\Sarit Hollander\\Desktop\\Study\\Year C\\Semester A\\IR\\Search Engine\\SearchEngine\\results_old')
        indexer.add_new_doc(p)
        expected = {"HELLO", "goodbye"}
        actual = set(indexer.inverted_idx.keys())

        self.assertEqual(expected, actual)

