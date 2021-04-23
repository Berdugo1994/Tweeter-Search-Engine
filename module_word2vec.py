from gensim.models import Word2Vec
import parser_module
import datetime
import numpy as np


class Word2vecModule:

    def __init__(self, model_dir, inverted_index, info_scalar=35, train=False):
        self.trained_model = None
        self.dic_docs = None
        self.dic_words = None
        self.file_saved_name = 'trained_word2vec_model'
        self.path = model_dir + "/" + self.file_saved_name
        self.fulltext_path = model_dir + "/" + 'corpus_full.txt'
        self.info_scalar = info_scalar
        self.dic_inverted_docs = inverted_index.get_docs_to_info_dict()
        self.train_model(train)  # will train the model only if train var is True !
        self.inverted_index = inverted_index
        self.build_dics(inverted_index)

    def train_model(self, train, num_of_docs=None):
        """
        run only once to train the model on the full corpus
        :param train: boolean param , if false func dont do anything.
        :param num_of_docs: in case off testing, to train on X number of docs.
        saves the model to a file named : file_saved_name = 'trained_word2vec_model_old'
        """
        if not train:
            return
        print("start train word2vec model from full text", datetime.datetime.now())
        file1 = open(self.fulltext_path, encoding='utf-8')
        lines = file1.readlines()
        parser = parser_module.Parse()
        sentences = []
        count = 0
        print("start parsing each document")
        for line in lines:
            before_lower_sen = parser.parse_sentence(line)
            sen = []
            for word in before_lower_sen:
                word_lower = word.lower()
                sen.append(word_lower)
            sentences.append(sen)
            count += 1
            if num_of_docs is not None and num_of_docs == count:  # if num of docs is declared. for example = 100000
                model = Word2Vec(sentences=sentences, size=self.info_scalar, sg=1, window=10, min_count=6, iter=2,
                                 workers=8)
                model.init_sims(replace=True)
                model.save(self.path)
                return
            if count % 50000 == 0:
                print("parser passed ", count, " of docs    ", datetime.datetime.now())
        print("start training the word2vec model     ", datetime.datetime.now())
        model = Word2Vec(sentences=sentences, size=self.info_scalar, sg=1, window=6, min_count=8, iter=10, workers=4)
        print("finish training the word2vec model     ", datetime.datetime.now())
        model.init_sims(replace=True)
        model.save(self.path)
        print("model built and saved successfuly to path -> ", self.path)

    def build_dics(self, inverted_idx):
        self.trained_model = Word2Vec.load(self.path)
        self.build_words_dic(inverted_idx)
        self.build_docs_dic()

    def build_words_dic(self, inverted_idx):
        """
        create a dictionary of {word: vector}
        """
        embeddings_dict = {}
        for word in self.trained_model.wv.vocab:
            if inverted_idx.is_term_exist(word.lower()) or inverted_idx.is_term_exist(word.upper()):
                vector = self.trained_model[word]
                embeddings_dict[word.lower()] = vector
        self.dic_words = embeddings_dict

    def build_docs_dic(self):
        """
        create a dictionary of {document: [(vector, score)]}
        """
        dic_docs_vecs = {}
        for doc_key in self.dic_inverted_docs.keys():
            dic_of_terms, doc_length, doc_date, full_text = self.dic_inverted_docs[doc_key]
            res_vec = self.vec_of_doc_by_dict(dic_of_terms)
            if res_vec is not None:
                dic_docs_vecs[doc_key] = res_vec
        self.dic_docs = dic_docs_vecs

    def vec_of_doc_by_dict(self, dic_terms):
        """
        given a dictionary of terms and their frequency in document and returns rep vec and glove score.
        :param dic_terms: dictionary of term and vector - {term: ['dog' - 2 , 'walk' -1 , 'breeze' -1 ,'drink' - 10]}
        :return: represent single vector
        """
        rep_vec = np.zeros(self.info_scalar)
        count_valid_terms = 0
        for word in dic_terms.keys():
            word_vec = self.dic_words.get(word.lower(), None)
            if word_vec is not None:
                tf = dic_terms[word]
                count_valid_terms += tf
                rep_vec += word_vec * tf
        if count_valid_terms == 0:
            return None
        average_vec = rep_vec / count_valid_terms
        return average_vec

    def vec_for_doc(self, doc_id):
        return self.dic_docs.get(doc_id, None)

    # Methods for using query expansion ***************************************************************************

    def find_similarity(self, word, num_of_similar=1):
        """
        find words that are similar to a term
        :param word: the term
        :param num_of_similar: amount of similar words to find, default is one
        :return: list of similar words
        """
        try:
            similarities = self.trained_model.wv.most_similar(word.lower())
        except:
            print("word", word, "not in word2vec vocabulary")
            return None
        result = []
        count = 0
        for word, score in similarities:
            result.append(word)
            count += 1
            if count >= num_of_similar:
                break
        return result

    def expanded_query_with_idf(self, query_as_list):
        """
        expand the query with similar words to the terms in query
        :param query_as_list: list of query's terms
        :return: the query with more similar terms in it
        """
        query_expanded = query_as_list
        word_freq_min = None
        word_to_expand = None
        if len(query_as_list) == 0:
            return query_as_list
        elif len(query_as_list) == 1:
            first_word = query_as_list[0]
            word = self.find_similarity(first_word, num_of_similar=2)
            if word is not None:
                query_expanded += word
                return query_expanded
        terms_freq = self.inverted_index.get_inverted_index()
        for word in query_as_list:
            word_freq = terms_freq.get(word, 0)
            if word_freq_min is None or word_freq < word_freq_min:
                word_freq_min = word_freq
                word_to_expand = word
        new_word = self.find_similarity(word_to_expand, num_of_similar=1)
        if new_word is not None:
            query_expanded += new_word
        return query_expanded
