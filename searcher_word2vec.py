import math

from scipy import spatial

from ranker import Ranker


# DO NOT MODIFY CLASS NAME
class Searcher:
    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit. The model
    # parameter allows you to pass in a precomputed model that is already in
    # memory for the searcher to use such as LSI, LDA, Word2vec models.
    # MAKE SURE YOU DON'T LOAD A MODEL INTO MEMORY HERE AS THIS IS RUN AT QUERY TIME.
    def __init__(self, parser, indexer, model=None):
        self._parser = parser
        self._indexer = indexer
        self.dic_docs = self._indexer.get_docs_to_info_dict()
        self.posting = self._indexer.get_posting_dict()
        self.inverted_index = self._indexer.get_inverted_index()
        self.average_doc_length = self._indexer.get_average_doc_length()
        self.num_of_tweets = len(self.dic_docs)
        self._ranker = Ranker(self.dic_docs)
        self._model = model

    # DO NOT MODIFY THIS SIGNATURE
    # You can change the internal implementation as you see fit.
    def search(self, query, k=None):
        """
        Executes a query over an existing index and returns the number of
        relevant docs and an ordered list of search results (tweet ids).
        parser the query and turn it into a list of terms,
        then find the k best results by invertedIndex.
        using word embedding  it calculates the distance between doc and query
        and then gives a 'bonus' to docs that has more than one match with query.

        Input:
            query - string.
            k - number of top results to return, default to everything.
        Output:
            A tuple containing the number of relevant search results, and
            a list of tweet_ids where the first element is the most relavant
            and the last is the least relevant result.
        """
        query_as_list = self._parser.parse_sentence(query)
        expanded_query_w = self._model.expanded_query_with_idf(query_as_list)
        if len(query_as_list) == 0:
            return 0, []
        tuples_tweet_sim = self.relevant_and_cosSim_vecs_with_bonuses(expanded_query_w)  # CosSim func
        if tuples_tweet_sim is None:
            return 0, []
        ranked_docs = self._ranker.simple_rank(tuples_tweet_sim, reversed=False)
        ranked_docs = self._ranker.retrieve_top_k(ranked_docs, k)
        return len(ranked_docs), ranked_docs

    def relevant_and_cosSim_vecs_with_bonuses(self, query_as_list):
        """
        calculates cosSim with word2Vec module.
        when using vectors distance - the smallest the distance, the better !
        :param query_as_list: query after parsing - list of strings
        :return: list of tuples
        """
        dic_key_sim = {}
        result_list = []
        N = self.num_of_tweets
        query_dic = dict()
        query_len = 0
        for i in query_as_list:
            query_dic[i.lower()] = query_dic.get(i.lower(), 0) + 1
            query_len += 1
        query_vec = self._model.vec_of_doc_by_dict(query_dic)
        if query_vec is None:
            return result_list
        for term in query_as_list:
            if term.lower() in self.posting:
                term = term.lower()
            elif term.upper() in self.posting:
                term = term.upper()
            else:
                continue
            df = self.inverted_index.get(term, 0)  # df is doc frequency - in how many docs this term mentioned
            # bonus = tf * idf / (query_len ** 2)
            idf = math.log(N / df, 5)
            posting_doc = self.posting[term]
            for doc_id, tf, doc_len in posting_doc:
                bonus = 0.13
                if doc_id in dic_key_sim:
                    dic_key_sim[doc_id] -= bonus
                else:
                    doc_vec = self._model.vec_for_doc(doc_id)
                    if doc_vec is not None:
                        dic_key_sim[doc_id] = spatial.distance.euclidean(query_vec, doc_vec) - bonus
        # dic_key_sim = self.bm25(query_as_list, dic_key_sim) # for using bm25
        for item in dic_key_sim.items():
            result_list.append((item[0], item[1]))
        return result_list

    # UNUSED FUNCTIONS ##################################################################################################

    def bm25(self, query_as_list, dic_key_sim):
        """
        similarity function that we found that did not have been well with our model. we don't use it.
        :param query_as_list:
        :param dic_key_sim: dic filled with similarities alreadu from cosSim.
        :return:
        """
        N = self.num_of_tweets
        query_dic = dict()
        for i in query_as_list:
            query_dic[i.lower()] = query_dic.get(i.lower(), 0) + 1
        k = 2
        b = 0.4
        for i in query_as_list:
            query_dic[i.lower()] = query_dic.get(i.lower(), 0) + 1
        for term in query_as_list:
            if term.lower() in self.posting:
                term = term.lower()
            elif term.upper() in self.posting:
                term = term.upper()
            else:
                continue
            df = self.inverted_index.get(term, 0)  # df is doc frequency - in how many docs this term mentioned
            idf = math.log(N / df, 5)
            posting_doc = self.posting[term]
            for doc_id, tf, doc_len in posting_doc:
                if doc_id in dic_key_sim:
                    mone = query_dic[term.lower()] * (k + 1) * tf
                    mechane = tf + k * (1 - b + b * doc_len / self.average_doc_length) * idf
                    dic_key_sim[doc_id] -= 1 * mone / mechane
                else:
                    print("problem")
        return dic_key_sim

    def relevant_and_cosSim_only_vecs(self, query_as_list):
        """
        calculates cosSim with word2Vec module vectors only. no other similarity funcs.
        :param query_as_list: query after parsing - list of strings
        :param k: sort
        :return:
        """
        dic_key_sim = {}
        result_list = []
        query_dic = dict()
        for i in query_as_list:
            query_dic[i.lower()] = query_dic.get(i, 0) + 1
        query_vec = self._model.vec_of_doc_by_dict(query_dic)
        if query_vec is None:
            return result_list
        for term in query_as_list:
            if term.lower() in self.posting:
                term = term.lower()
            elif term.upper() in self.posting:
                term = term.upper()
            else:
                continue
            posting_doc = self.posting[term]
            for doc_id, tf, doc_len in posting_doc:
                if doc_id in dic_key_sim:
                    continue
                if doc_id not in dic_key_sim.keys():
                    doc_vec = self._model.vec_for_doc(doc_id)
                    if doc_vec is not None:
                        dic_key_sim[doc_id] = spatial.distance.euclidean(query_vec, doc_vec)
        for item in dic_key_sim.items():
            result_list.append((item[0], item[1]))
        return result_list

        # feel free to change the signature and/or implementation of this function
        # or drop altogether.

    def relevant_and_cosSim(self, query, k=None):
        """
        This function detect the relevant docs that might be good answer.
        IMPORTANT : we do here semi ranking by func of (num of each q_term in doc + num of terms belongs to query)
        the flow is such that -> we iterate on every term in query, check his posting , updating the relevant docs,(by
        mone and mechane) and move to the next term,until finishes the query list. by this we not pass even once
        a doc that has no shared words with the query.
        after finish pass all the words in term , we iterate the dictionary and sqrt the relevant parts of the equation.
        :param query: query
        :return: dictionary of relevant documents.
        """
        dic_key_sim = {}
        N = self.num_of_tweets
        for term in query:
            if term.lower() in self.posting:
                term = term.lower()
            elif term.upper() in self.posting:
                term = term.upper()
            else:
                continue
            df = self.inverted_index.get(term, 0)  # df is doc frequency - in how many docs this term mentioned
            posting_doc = self.posting[term]
            idf = math.log(N / df, 2)
            for doc_tuple in posting_doc:
                tf = doc_tuple[1] / doc_tuple[2]
                cos_sin_similarity_mone = (tf * idf)
                if doc_tuple[0] not in dic_key_sim.keys():
                    dic_key_sim[doc_tuple[0]] = [cos_sin_similarity_mone,
                                                 self.calculate_wij_mehane(doc_tuple[0], len(query))]
                else:
                    dic_key_sim[doc_tuple[0]][0] += cos_sin_similarity_mone
        sorted_results = \
            sorted(dic_key_sim.items(), key=lambda item: item[1][0] / item[1][1], reverse=True)
        if k is not None:
            sorted_results = sorted_results[0:k]
        result_list = []
        for item in sorted_results:
            result_list.append((item[0], item[1][0] / item[1][1]))
        return result_list

    def relevant_and_cosSim_with_bonuses(self, query, k=None):
        """
        This function detect the relevant docs that might be good answer.
        IMPORTANT : we do here semi ranking by func of (num of each q_term in doc + num of terms belongs to query)
        the flow is such that -> we iterate on every term in query, check his posting , updating the relevant docs,(by
        mone and mechane) and move to the next term,until finishes the query list. by this we not pass even once
        a doc that has no shared words with the query.
        after finish pass all the words in term , we iterate the dictionary and sqrt the relevant parts of the equation.
        :param query: query
        :return: dictionary of relevant documents.
        """
        dic_key_sim = {}
        N = self.num_of_tweets
        for term in query:
            if term.lower() in self.posting:
                term = term.lower()
            elif term.upper() in self.posting:
                term = term.upper()
            else:
                continue
            df = self.inverted_index.get(term, 0)  # df is doc frequency - in how many docs this term mentioned
            posting_doc = self.posting[term]
            idf = math.log(N / df, 2)
            for doc_tuple in posting_doc:
                tf = doc_tuple[1] / doc_tuple[2]
                cos_sin_similarity_mone = (tf * idf)
                if doc_tuple[0] not in dic_key_sim.keys():
                    dic_key_sim[doc_tuple[0]] = [cos_sin_similarity_mone,
                                                 self.calculate_wij_mehane(doc_tuple[0], len(query))]
                else:
                    dic_key_sim[doc_tuple[0]][0] += cos_sin_similarity_mone + 0.2
        sorted_results = \
            sorted(dic_key_sim.items(), key=lambda item: item[1][0] / item[1][1], reverse=True)
        if k is not None:
            sorted_results = sorted_results[0:k]
        result_list = []
        for item in sorted_results:
            result_list.append((item[0], item[1][0] / item[1][1]))
        return result_list

    def relevant_and_cosSim_without_length(self, query, k=None):
        """
        This function detect the relevant docs that might be good answer.
        IMPORTANT : we do here semi ranking by func of (num of each q_term in doc + num of terms belongs to query)
        the flow is such that -> we iterate on every term in query, check his posting , updating the relevant docs,(by
        mone and mechane) and move to the next term,until finishes the query list. by this we not pass even once
        a doc that has no shared words with the query.
        after finish pass all the words in term , we iterate the dictionary and sqrt the relevant parts of the equation.
        :param query: query
        :return: dictionary of relevant documents.
        """
        dic_key_sim = {}
        N = self.num_of_tweets
        for term in query:
            if term.lower() in self.posting:
                term = term.lower()
            elif term.upper() in self.posting:
                term = term.upper()
            else:
                continue
            df = self.inverted_index.get(term, 0)  # df is doc frequency - in how many docs this term mentioned
            posting_doc = self.posting[term]
            idf = math.log(N / df, 2)
            for doc_tuple in posting_doc:
                tf = doc_tuple[1]
                cos_sin_similarity_mone = (tf * idf)
                if doc_tuple[0] not in dic_key_sim.keys():
                    dic_key_sim[doc_tuple[0]] = [cos_sin_similarity_mone,
                                                 self.calculate_wij_mehane(doc_tuple[0], len(query))]
                else:
                    dic_key_sim[doc_tuple[0]][0] += cos_sin_similarity_mone + 0.11 * math.sqrt(tf)
        sorted_results = \
            sorted(dic_key_sim.items(), key=lambda item: item[1][0] / item[1][1], reverse=True)
        if k is not None:
            sorted_results = sorted_results[0:k]
        result_list = []
        for item in sorted_results:
            result_list.append((item[0], item[1][0] / item[1][1]))
        return result_list

    def relevant_docs(self, query):
        relevant = set()
        for term in query:
            if term.lower() in self.posting:
                term = term.lower()
            elif term.upper() in self.posting:
                term = term.upper()
            else:
                continue
            posting_doc = self.posting[term]
            for doc_tuple in posting_doc:
                relevant.add(doc_tuple[0])
        return relevant

    def calculate_wij_mehane(self, doc_id, query_len):
        doc_dic, doc_len, date, full_text = self.dic_docs[doc_id]
        total_wij_squared = 0
        for term in doc_dic.keys():
            if term.lower() in self.posting:
                term_at_post = term.lower()
            elif term.upper() in self.posting:
                term_at_post = term.upper()
            else:
                continue
            df = self.inverted_index.get(term_at_post, 0)  # df is doc frequency - in how many docs this term mentioned
            idf = math.log(self.num_of_tweets / df, 2)
            wij = (doc_dic[term] / doc_len) * idf
            total_wij_squared += wij ** 2
        total_wij_squared = math.sqrt(total_wij_squared * query_len)
        return total_wij_squared
