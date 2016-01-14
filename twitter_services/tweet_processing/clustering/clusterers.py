import json
import pandas

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
import DjangoSetup
from twitter_services.models import Tweet
from twitter_services.tweet_processing.normalizing import TweetNormalizer


class KMeansClusterer():
    def __init__(self, **kwargs):
        if kwargs['cluster_count'] is None:
            self.cluster_count = 4
        else:
            self.cluster_count = kwargs['cluster_count']
        self.km = KMeans(n_clusters=self.cluster_count)
        self.tweets_texts = None
        self.tfidf_matrix = None
        self.terms = None

    def cluster_tweets(self, **kwargs):
        related_entity = kwargs['related_entity']
        # dimension = kwargs['reputation_dimension']

        # Fetch tweets from the corpus
        self.tweets_texts = [json.loads(obj['json_str'])['text']
                             for obj in Tweet.objects.filter(related_entity=related_entity, ).values('json_str')]

        # Build vectorizer and matrix
        tfidf_vectorizer = TfidfVectorizer(max_features=200000, min_df=0.1, stop_words='english',
                                   use_idf=True, tokenizer=TweetNormalizer.normalize_texts, ngram_range=(1,3))
        self.tfidf_matrix = tfidf_vectorizer.fit_transform(self.tweets_texts)

        # # Feature names are just words that build up the vector
        self.terms = tfidf_vectorizer.get_feature_names()
        # print tfidf_matrix.shape

        # Try out K-Means clustering
        return self.km.fit(self.tfidf_matrix)

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
    clusterer = KMeansClusterer(cluster_count=4)
    clusterer.cluster_tweets(related_entity='Apple')
    clusterer.print_results()
