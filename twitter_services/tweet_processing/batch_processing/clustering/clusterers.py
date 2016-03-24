import pandas
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

if __name__ == '__main__':
    import os
    import django
    os.environ['DJANGO_SETTINGS_MODULE'] = 'TwitterRepManagement.settings'
    django.setup()

from twitter_services.models import Tweet
from twitter_services.tweet_processing.normalizing import TweetNormalizer


# The class that handles tweets clustering.
# It takes related entity, dimension and cluster count as input, and returns tweets for each clusters
class KMeansClusterer():
    def __init__(self, **kwargs):
        if kwargs['cluster_count'] is None:
            self.cluster_count = 1
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
        dimension = kwargs['reputation_dimension']
        time_threshold = kwargs['time_threshold']

        # Fetch tweets from the corpus
        self.tweets_objects = [tweet for tweet
                               in Tweet.objects.all().filter(tweet__related_entity=related_entity,
                                                             tweet__reputation_dimension=dimension,
                                                             created_at__gt=time_threshold)]
        self.tweets_texts = [obj.tweet['text'] for obj in self.tweets_objects]

        # Build vectorizer and matrix
        tfidf_vectorizer = TfidfVectorizer(max_features=200000, min_df=0.1, stop_words='english',
                                           use_idf=True,
                                           tokenizer=TweetNormalizer.get_tokens,
                                           ngram_range=(1,3))
        self.tfidf_matrix = tfidf_vectorizer.fit_transform(self.tweets_texts)

        # # Feature names are just words that build up the vector
        self.terms = tfidf_vectorizer.get_feature_names()
        # print tfidf_matrix.shape

        # Try out K-Means clustering
        self.clusters = self.km.fit_predict(self.tfidf_matrix)

    def get_tweets_clustered(self):
        tweets_clustered = []
        for i in range(self.cluster_count):
            clusters_n = np.where(self.clusters == i)[0]
            tweets = [self.tweets_objects[i] for i in clusters_n]
            tweets_clustered.append(tweets)
        return tweets_clustered

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
    from datetime import datetime, timedelta
    import pytz

    clusterer = KMeansClusterer(cluster_count=5)
    clusterer.cluster_tweets(related_entity='Apple',
                             reputation_dimension='Products & Services',
                             time_threshold=datetime.now(pytz.utc) - timedelta(days=1))
    clusterer.print_results()

