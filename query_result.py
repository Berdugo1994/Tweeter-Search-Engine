class QueryResult:

    def __init__(self,
                 tweet_id,
                 similarity,
                 full_text):
        self.tweet_id = tweet_id
        self.similarity = similarity
        self.full_text = full_text

    def __str__(self):
        # return ", Tweet id: " + self.tweet_id + ", Score: " + str(self.similarity)
        return self.full_text + ", Tweet id: " + self.tweet_id + ", Score: " + str(self.similarity)