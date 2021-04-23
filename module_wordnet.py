import nltk
from nltk.corpus import wordnet


class WordnetModule:

    def __init__(self, model_dir):
        self.model_dir = model_dir

    def query_expanded(self, query_as_list):
        """
        expand the query with similar words to the terms in query
        :param query_as_list: list of query's terms
        :return: the query with more similar terms in it
        """
        if len(query_as_list) == 0:
            return query_as_list
        synonyms = list(query_as_list)

        for term in query_as_list[:2]:
            self.add_synonyms(synonyms, term, 1)

        return synonyms

    def add_synonyms(self, synonyms, term, amount=1):
        """
        adding similar words to term
        :param synonyms: list of query terms
        :param term: the term to find similar words to
        :param amount: amount of words to add to query list with this term
        """
        current = 0
        for syn in wordnet.synsets(term):
            for lemma in syn.lemmas():
                if lemma.name() not in synonyms:
                    synonyms.append(lemma.name())
                    current += 1
                    if current == amount:
                        return
