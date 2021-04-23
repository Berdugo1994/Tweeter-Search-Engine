import math

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
        then find the k best results by cosSim.
        then calculate it with GloVe model weight.
        Input:
            query - string.
            k - number of top results to return, default to everything.
        Output:
            A tuple containing the number of relevant search results, and
            a list of tweet_ids where the first element is the most relavant
            and the last is the least relevant result.
        """
        query_as_list = self._parser.parse_sentence(query)
        expanded_query = self._model.query_expanded(query_as_list)
        if len(query_as_list) == 0:
            return 0, []

        tuples_tweet_sim = self.relevant_and_cosSim(expanded_query)  # CosSim func
        if tuples_tweet_sim is None:
            return 0, []
        ranked_docs = self._ranker.simple_rank(tuples_tweet_sim, reversed=True)
        ranked_docs = self._ranker.retrieve_top_k(ranked_docs, k)
        return len(ranked_docs), ranked_docs

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
            idf = math.log(N / df, 10)
            for doc_tuple in posting_doc:
                tf = doc_tuple[1] / doc_tuple[2]
                cos_sin_similarity_mone = (tf * idf)
                if doc_tuple[0] not in dic_key_sim.keys():
                    dic_key_sim[doc_tuple[0]] = [cos_sin_similarity_mone,
                                                 self.calculate_wij_mehane(doc_tuple[0], len(query))]
                else:
                    dic_key_sim[doc_tuple[0]][0] += cos_sin_similarity_mone
        result_list = []
        for item in dic_key_sim.items():
            result_list.append((item[0], item[1][0] / item[1][1]))
        return result_list

    def calculate_wij_mehane(self, doc_id, query_len):
        """
        calculate vector size for cosSin similarity score
        :param doc_id: document id
        :param query_len: size of the query
        :return: vector size
        """
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
            idf = math.log(self.num_of_tweets / df, 10)
            wij = (doc_dic[term] / doc_len) * idf
            total_wij_squared += wij ** 2
        total_wij_squared = math.sqrt(total_wij_squared * query_len)
        return total_wij_squared
