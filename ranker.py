# you can change whatever you want in this module, just make sure it doesn't 
# break the searcher module
from query_result import QueryResult


class Ranker:
    def __init__(self, docs_to_info_dict):
        self.docs_to_info_dict = docs_to_info_dict

    # glove ranker
    def rank_relevant_doc(self,
                          lst_tup_tweet_sim,
                          dic_tweet_glove,
                          max_glove_dis,
                          cos_sim_weight=1,
                          glove_sim_weight=0):
        """
        glove ranker - calculate the score for each doc
        :param lst_tup_tweet_sim: list of (tweet_id, similarity)
        :param dic_tweet_glove: dictionary of (distance, glove weight)
        :param max_glove_dis: maximum distance of glove
        :param cos_sim_weight: the weight of cosSin similarity in the score calculation
        :param glove_sim_weight: the weight of glove in the score calculation
        :return: list of all relevant documents
        """
        relevant_docs_finally = []
        for tweet_id, similarity_cosSim in lst_tup_tweet_sim:
            try:
                cos_sim_impact = cos_sim_weight * similarity_cosSim
                glove_dis, glove_match_per = dic_tweet_glove.get(tweet_id, 0)
                glove_value = glove_sim_weight * max_glove_dis * glove_match_per
                glove_impact = glove_sim_weight * (max_glove_dis - glove_dis) * glove_match_per
                full_similarity = (cos_sim_impact + glove_impact) / (cos_sim_weight + glove_value)
                full_text = self.docs_to_info_dict[tweet_id][3]
                relevant_docs_finally.append(
                    QueryResult(tweet_id=tweet_id,
                                similarity=full_similarity,
                                full_text=full_text))
            except:
                print('tweet_id {} not found in docs'.format(tweet_id))

        sorted(relevant_docs_finally, key=lambda item: item.similarity, reverse=True)
        relevant_docs_by_id = []
        for i in range(len(relevant_docs_finally)):
            relevant_docs_by_id.append(relevant_docs_finally[i].tweet_id)
        return relevant_docs_by_id

    # word2vec ranker
    def simple_rank(self, lst_tup_tweet_sim, reversed):
        """
        word2vec ranker - calculate the score for each doc
        :param lst_tup_tweet_sim: list of (document, similarity)
        :param reversed: boolean to if sorting relevant documents list in reverse
        :return: list of all relevant documents
        """
        relevant_docs_finally = []
        for tweet_id, similarity_cosSim in lst_tup_tweet_sim:
            try:
                full_text = self.docs_to_info_dict[tweet_id][3]
                relevant_docs_finally.append(
                    QueryResult(tweet_id=tweet_id,
                                similarity=similarity_cosSim,
                                full_text=full_text))
            except:
                print('tweet_id {} not found in docs'.format(tweet_id))

        relevant_docs_finally = sorted(relevant_docs_finally, key=lambda item: item.similarity, reverse=reversed)
        relevant_docs_by_id = []
        for i in range(len(relevant_docs_finally)):
            relevant_docs_by_id.append(relevant_docs_finally[i].tweet_id)
        return relevant_docs_by_id

    @staticmethod
    def retrieve_top_k(sorted_relevant_doc, k=None):
        """
        return a list of top K tweets based on their ranking from highest to lowest
        :param sorted_relevant_doc: list of all candidates docs.
        :param k: Number of top document to return
        :return: list of relevant document
        """
        if k is None:
            return sorted_relevant_doc
        return sorted_relevant_doc[:k]
