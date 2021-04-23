import pandas as pd
import search_engine_best
def turn_to_parquet():
    df = pd.read_csv('testing/testing_results/ques1.csv')
    df.to_parquet('testing/testing_results/ques1.parquet')

def using_our_testing():
    se = search_engine_best.SearchEngine()
    se._parser.stop_words=["to", "the", "and", "a", "very", "of", "would", "are", ",", "!", "?"]
    se.build_index_from_parquet("testing/testing_results/ques1.parquet")
    se.load_precomputed_model('model/glove.twitter.27B.25d.txt')
    se.load_index("idx_bench")
    results = se.search("?everyone I like are haters and losers")
    # for i in range(len(results[1])):
    #     print(results[1][i].tweet_id ,results[1][i].similarity)


if __name__ == '__main__':
    turn_to_parquet()
    using_our_testing()
