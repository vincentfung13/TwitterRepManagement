from clustering.clusterers import KMeansClusterer
from topic_extracting.topic_extractors import LDATopicExtractor
from twitter_services.tweet_processing import utility


class ReputationMonitor(object):
    def __init__(self):
        self.clusterer = KMeansClusterer(cluster_count=5)

    def scan(self):
        for entity in utility.entities_list:
            try:
                self.clusterer.cluster_tweets(related_entity=entity)
                tweets_clusters = self.clusterer.get_tweets_clustered()
                for cluster in tweets_clusters:
                    negative_count = 0
                    tweets_count = len(cluster)
                    notify = False

                    for tweet in cluster:
                        if negative_count > tweets_count/2:
                            notify = True
                            break

                        if utility.is_negative(tweet.sentiment_score):
                            negative_count += 1

                    if notify:
                        try:
                            topic_extractor = LDATopicExtractor(cluster)
                            print topic_extractor.extract_topic()
                            # TODO: dispatch notification
                            self.__notify__()
                        except ValueError:
                            print 'No tweet in the cluster'
            except ValueError:
                print 'No tweet for the entity %s' % entity

    @staticmethod
    def __notify__():
        # TODO: Dispatch message to the front end (or sending other kinds of alerts)
        print 'Send alert!'

if __name__ == '__main__':
    monitor = ReputationMonitor()
    monitor.scan()
