import json
import pandas

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from twitter_services.models import Tweet
from twitter_services.tweet_processing.normalizing import TweetNormalizer

# Fetch tweets from corpus
all_tweets_words = \
    [json.loads(obj['tweet_json'])['text'] for obj in Tweet.objects.values('tweet_json')
     if json.loads(obj['tweet_json'])['entity'] == 'Apple']

tfidf_vectorizer = TfidfVectorizer(max_features=200000, min_df=0.1, stop_words='english',
                                   use_idf=True, tokenizer=TweetNormalizer.normalize_texts, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(all_tweets_words)
terms = tfidf_vectorizer.get_feature_names()

print tfidf_matrix.shape

dist = 1 - cosine_similarity(tfidf_matrix)

# Trying out K-Means clustering
num_cluster = 4
km = KMeans(n_clusters=num_cluster)
km.fit(tfidf_matrix)
clusters = km.labels_.tolist()


tweets = {'text': all_tweets_words, 'clusters': clusters}
frame = pandas.DataFrame(tweets, index=[clusters])

print frame['clusters'].value_counts()

order_centroids = km.cluster_centers_.argsort()[:, ::-1]

for i in range(num_cluster):
    print 'Top 6 words for cluster %d: ' % i
    for ind in order_centroids[i, :6]:
        print terms[ind] + ', ',
    print
