# DO NOT MODIFY CLASS NAME
import copy
import itertools

from numpy import take

import utils


class Indexer:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def __init__(self, config):
        self.inverted_idx = {}
        self.postingDict = {}
        self.docs_to_info_dict = {}
        self.config = config
        self.num_of_tweets = 0
        self.total_num_of_words = 0

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def add_new_doc(self, document):
        """
        This function perform indexing process for a document object.
        Saved information is captures via two dictionaries ('inverted index' and 'posting')
        :param document: a document need to be indexed.
        :return: -
        """
        self.num_of_tweets += 1
        document_dictionary = document.term_doc_dictionary
        dict_keys = list(document_dictionary.keys())
        # Go over each term in the doc
        for term in dict_keys:
            original_term = term
            lower_term = term.lower()
            # Check if the word is upper case
            if term[0].isupper():
                # If now upper but is actually lower
                if lower_term in self.inverted_idx or lower_term in document_dictionary:
                    if lower_term not in document_dictionary:
                        document_dictionary[lower_term] = 0
                    document_dictionary[lower_term] += document_dictionary[original_term]
                    del document_dictionary[original_term]

        if document.doc_length > 0:
            self.total_num_of_words += document.doc_length
            self.docs_to_info_dict[document.tweet_id] = (document_dictionary,
                                                         document.doc_length,
                                                         document.tweet_date,
                                                         document.full_text)

        # Go over each term in the doc
        for term in document_dictionary.keys():
            original_term = term
            lower_term = term.lower()
            upper_term = term.upper()
            # Check if the word is upper case
            if term[0].isupper():
                # If now upper but is actually lower
                if lower_term in self.inverted_idx:
                    # Save as lower
                    term = lower_term
                # If upper and was'nt lower before - save as upper
                else:
                    term = upper_term
                    # If Term is lower
            elif term[0].islower() and lower_term != upper_term:
                # Save as lower
                term = lower_term
                # If previous upper is in dictionary - need to lower it in all dicts and existing files
                if upper_term in self.inverted_idx:
                    # Fixing inverted index
                    self.inverted_idx[lower_term] = self.inverted_idx[upper_term]
                    del self.inverted_idx[upper_term]
                    # Fixing current posting dict
                    if upper_term in self.postingDict:
                        self.postingDict[lower_term] = self.postingDict[upper_term]
                        del self.postingDict[upper_term]

            try:
                # Update inverted index and posting
                if term not in self.inverted_idx.keys():
                    self.inverted_idx[term] = 1
                    self.postingDict[term] = []
                else:
                    self.inverted_idx[term] += 1

                if term not in self.postingDict:
                    self.postingDict[term] = []

                # 15252 -> the lion sleeps at lion house
                # this is how term will keep each doc. "lion - >[(15252,2,6)]
                self.postingDict[term].append(
                    (document.tweet_id, document_dictionary[original_term], document.doc_length))
            except:
                print('problem with the following key {}'.format(term[0]))

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def load_index(self, fn):
        """
        Loads a pre-computed index (or indices) so we can answer queries.
        Input:
            fn - file name of pickled index.
        """
        self.inverted_idx, self.postingDict, self.docs_to_info_dict = utils.load_obj(fn)
        self.num_of_tweets = len(self.docs_to_info_dict)
        self.total_num_of_words = len(self.inverted_idx)

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def save_index(self, fn):
        """
        Saves a pre-computed index (or indices) so we can save our work.
        Input:
              fn - file name of pickled index.
        """
        utils.save_obj((self.inverted_idx, self.postingDict, self.docs_to_info_dict), fn)

    # feel free to change the signature and/or implementation of this function
    # or drop altogether.
    def is_term_exist(self, term):
        """
        Checks if a term exist in the dictionary.
        """
        return term in self.postingDict

    # feel free to change the signature and/or implementation of this function
    # or drop altogether.
    def get_term_posting_list(self, term):
        """
        Return the posting list from the index for a term.
        """
        return self.postingDict[term] if self.is_term_exist(term) else []

    def get_docs_to_info_dict(self):
        """
        :return:Dictionary of all docs such: {'doc_id1' -> (document_dictionary, document.doc_length, document.tweet_date, full text),
                                            'doc_id2' -> (document_dictionary, document.doc_length, document.tweet_date,full text),
                                            ...}

        """
        return self.docs_to_info_dict

    def get_posting_dict(self):
        return self.postingDict

    def get_inverted_index(self):
        return self.inverted_idx

    def limit_words(self, words_limit):
        """
        limit the inverted index dictionary by words_limit, if the term dictionary is bigger than the limit,
        keep the most frequent words
        """
        if len(self.inverted_idx) > words_limit:
            sorted_inverted_dict = dict(sorted(self.inverted_idx.items(), key=lambda item: item[1], reverse=True))
            self.inverted_idx = dict(list(sorted_inverted_dict.items())[:words_limit])
            temp_posting = copy.deepcopy(self.postingDict)
            for key in temp_posting.keys():
                if key not in self.inverted_idx:
                    del self.postingDict[key]

    def get_average_doc_length(self):
        return self.total_num_of_words / self.num_of_tweets
