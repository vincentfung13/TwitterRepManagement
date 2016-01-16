import json
import pandas
import numpy as np

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import DjangoSetup
from twitter_services.models import Tweet
from twitter_services.tweet_processing.normalizing import TweetNormalizer


class KMeansClusterer():
    def __init__(self, **kwargs):
        if kwargs['cluster_count'] is None:
            self.cluster_count = 8
        else:
            self.cluster_count = kwargs['cluster_count']
        self.km = KMeans(n_clusters=self.cluster_count)
        self.tweets_objects = None
        self.tweets_texts = None
        self.tfidf_matrix = None
        self.terms = None
        self.clusters = None

    def cluster_tweets(self, **kwargs):
        related_entity = kwargs['related_entity']
        # dimension = kwargs['reputation_dimension']

        # Fetch tweets from the corpus
        self.tweets_objects = [tweet for tweet
                               in Tweet.objects.all().filter(related_entity=related_entity, )]
        self.tweets_texts = [json.loads(obj.json_str)['text'] for obj in self.tweets_objects]

        # Build vectorizer and matrix
        tfidf_vectorizer = TfidfVectorizer(max_features=200000, min_df=0.1, stop_words='english',
                                   use_idf=True, tokenizer=TweetNormalizer.normalize_texts, ngram_range=(1,3))
        self.tfidf_matrix = tfidf_vectorizer.fit_transform(self.tweets_texts)

        # # Feature names are just words that build up the vector
        self.terms = tfidf_vectorizer.get_feature_names()
        # print tfidf_matrix.shape

        # Try out K-Means clustering
        self.clusters = self.km.fit_predict(self.tfidf_matrix)

    def get_tweets_cluster(self, cluster):
        clusters_n = np.where(self.clusters == cluster)[0]
        print clusters_n, len(self.tweets_objects)
        tweets = [self.tweets_objects[i] for i in clusters_n]
        return tweets

    def print_results(self):
        print self.tfidf_matrix.shape

        tweets = {'text': self.tweets_texts, 'clusters': self.km.labels_.tolist()}
        frame = pandas.DataFrame(tweets, index=[self.km.labels_.tolist()])

        print frame['clusters'].value_counts()
        order_centroids = self.km.cluster_centers_.argsort()[:, ::-1]

        for i in range(self.cluster_count):
            print 'Top 6 words for cluster %d: ' % i
            for ind in order_centroids[i, :6]:
                print self.terms[ind] + ', ',
            print

if __name__ == '__main__':
    clusterer = KMeansClusterer(cluster_count=8)
    clusterer.cluster_tweets(related_entity='Apple')
    clusterer.print_results()
