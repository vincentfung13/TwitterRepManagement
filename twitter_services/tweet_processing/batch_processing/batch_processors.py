from clustering.clusterers import KMeansClusterer
from topic_extracting.topic_extractors import LDATopicExtractor
from twitter_services.tweet_processing import utility
from user_handle.models import UserMessage


class ReputationMonitor(object):
    def __init__(self):
        self.clusterer = KMeansClusterer(cluster_count=5)

    # Nasty three-nested loop
    def scan(self):
        for entity in utility.entities_list:
            print 'Entity: %s' % entity
            for reputation_dimension in utility.dimension_list:
                print '\t Dimension %s' % reputation_dimension
                try:
                    self.clusterer.cluster_tweets(related_entity=entity, reputation_dimension=reputation_dimension)
                    tweets_clusters = self.clusterer.get_tweets_clustered()
                    for cluster in tweets_clusters:
                        negative_count = 0
                        tweets_count = len(cluster)
                        notify = False

                        # Count negative tweets in each cluster
                        for tweet in cluster:
                            if negative_count > tweets_count * 0.3:
                                print negative_count, tweets_count
                                notify = True
                                break

                            if utility.is_negative(tweet.sentiment_score):
                                negative_count += 1

                        if notify:
                            try:
                                topic_extractor = LDATopicExtractor(cluster)
                                print '\t\t cluster_topic: %s' % topic_extractor.extract_topic()
                                self.__notify__()
                            except ValueError:
                                print '\t\t No tweet in the cluster'
                except ValueError:
                    print '\t No tweet for the entity %s' % entity

    @staticmethod
    def __notify__():
        # TODO: Dispatch message to the front end (or sending other kinds of alerts)
        print '\t\t Reputation issue'
        pass

if __name__ == '__main__':
    monitor = ReputationMonitor()
    monitor.scan()
