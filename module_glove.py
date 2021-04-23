from scipy import spatial
import numpy as np


class GloVe:
    def __init__(self, inverted_idx, info_scalar=25):
        # TODO: check
        self.file_saved_name = 'glove.twitter.27B.25d.txt'
        self.path_to_model = '../../../../glove.twitter.27B.25d.txt'
        self.info_scalar = info_scalar
        self.inverted_idx = inverted_idx
        self.dic_inverted_docs = self.inverted_idx.get_docs_to_info_dict()
        self.dic_words = self.build_words_dic(self.inverted_idx)
        self.dic_docs = self.build_docs_dic()

    def build_words_dic(self, inverted_idx):
        """
        create a dictionary of {word: vector}
        """
        embeddings_dict = {}
        vec_len = self.info_scalar
        with open(self.path_to_model, 'r', encoding="utf-8") as f:
            for line in f:
                values = line.split()
                word = values[0]
                if inverted_idx.is_term_exist(word.lower()) or inverted_idx.is_term_exist(word.upper()):
                    vector = np.asarray(values[1:vec_len], "float32")
                    embeddings_dict[word] = vector
        return embeddings_dict

    def build_docs_dic(self):
        """
        create a dictionary of {document: [(vector, score)]}
        """
        dic_docs_vecs = {}
        for doc_key in self.dic_inverted_docs.keys():
            dic_of_terms, doc_length, doc_date, full_text = self.dic_inverted_docs[doc_key]
            result_tup = self.vec_of_doc(dic_of_terms, doc_length)
            if result_tup[0] is not None:
                dic_docs_vecs[doc_key] = result_tup
        return dic_docs_vecs

    def relative_score_query_docs(self, query, docs_list_with_cosSim):
        """
        :param query: a list of terms.[String,String,String]
        :param docs_list_with_cosSim: list of docs_ids(String,String,String)
        the function returns list of tuples. each tuple is (distance*float*,glove weight *float*)
        """
        query_dic = dict()
        for i in query:
            query_dic[i.lower()] = query_dic.get(i, 0) + 1
        query_vec, query_glove_score = self.vec_of_doc(query_dic, len(query))
        dic_doc_query_glove = dict()
        max_glove_dis = 0
        default_glove_weight = 0.1
        default_glove_vec = spatial.distance.euclidean(query_vec, np.zeros(24))
        for doc_id, cosSim in docs_list_with_cosSim:
            if doc_id in self.dic_docs:
                doc_vec, doc_glove_score = self.dic_docs[doc_id]
                glove_doc_query_weight = doc_glove_score * query_glove_score
                glove_doc_query_distance = spatial.distance.euclidean(query_vec, doc_vec)
                if max_glove_dis < glove_doc_query_distance:
                    max_glove_dis = glove_doc_query_distance
                glove_doc_query_weight = max(default_glove_weight, glove_doc_query_weight)
                dic_doc_query_glove[doc_id] = (
                    glove_doc_query_distance, glove_doc_query_weight)  # the smallest the distance, the better !
            else:
                dic_doc_query_glove[doc_id] = (
                    default_glove_vec, default_glove_weight)  # the smallest the distance, the better !
        return dic_doc_query_glove, max_glove_dis

    def vec_of_doc(self, dic_terms, doc_length):
        """
        given a dictionary of terms and their frequency in document and returns rep vec and glove score.
        :param dic_terms:dictionary of term and vector - {term: ['dog' - 2 , 'walk' -1 , 'breeze' -1 ,'drink' - 10]}
        :param doc_length: document size
        :return: tuple of (vector, score)
        """
        rep_vec = np.zeros(24)
        count_valid_terms = 0
        for word in dic_terms.keys():
            word_vec = self.dic_words.get(word.lower(), None)
            if word_vec is not None:
                tf = dic_terms[word]
                count_valid_terms += tf
                rep_vec += word_vec * tf
        if count_valid_terms == 0:
            return rep_vec, 0
        glove_score = count_valid_terms / doc_length
        average_vec = rep_vec / count_valid_terms
        return average_vec, glove_score
