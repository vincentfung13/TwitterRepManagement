from clustering.clusterers import KMeansClusterer
from topic_extracting.topic_extractors import LDATopicExtractor
from twitter_services.tweet_processing import utility
from user_handle import utility as user_util
from user_handle.models import Message, UserMessage, UserEntity
from django.db import transaction
from datetime import datetime, timedelta
from twitter_services.tweet_processing.batch_processing.statistics import Statistics
from twitter_services.models import Statistics as Tweet_Stat_Table
import pytz


class ReputationMonitor(object):
    def __init__(self):
        self.clusterer = KMeansClusterer(cluster_count=5)
        self.period_days = 1

    # Nasty three-nested loop
    def scan(self):
        time_threshold = datetime.now(pytz.utc) - timedelta(days=self.period_days)
        for entity in utility.entities_list:
            print 'Entity: %s' % entity
            # Get statistics for whole entity and write results to the database
            statistics_dict_whole = Statistics.get_stats(time_threshold, entity)
            Tweet_Stat_Table.objects.create(related_entity=entity,
                                            total_tweets_count=statistics_dict_whole['total_tweets_count'],
                                            negative_count=statistics_dict_whole['negative_count'],
                                            reputation_score=statistics_dict_whole['reputation_score'])

            for reputation_dimension in utility.dimension_list:
                # Get statistics for each dimension of entities and write results to the database
                statistics_dict_dimension = Statistics.get_stats(time_threshold, entity, dimension=reputation_dimension)
                Tweet_Stat_Table.objects.create(related_entity=entity,
                                                reputation_dimension=reputation_dimension,
                                                total_tweets_count=statistics_dict_dimension['total_tweets_count'],
                                                negative_count=statistics_dict_dimension['negative_count'],
                                                reputation_score=statistics_dict_dimension['reputation_score'])

                # Clustering, extract topics and send out alerts
                print '\t Dimension %s' % reputation_dimension
                try:
                    time_threshold = datetime.now(pytz.utc) - timedelta(hours=self.period_hours)
                    self.clusterer.cluster_tweets(related_entity=entity,
                                                  reputation_dimension=reputation_dimension,
                                                  time_threshold=time_threshold)
                    tweets_clusters = self.clusterer.get_tweets_clustered()
                    for cluster in tweets_clusters:
                        negative_count = 0
                        tweets_count = len(cluster)
                        notify = False

                        # Count negative tweets in each cluster
                        for tweet_orm in cluster:
                            if negative_count > tweets_count * 0.5:
                                print negative_count, tweets_count
                                notify = True
                                break

                            if utility.is_negative(tweet_orm.tweet['sentiment_score']):
                                negative_count += 1

                        if notify:
                            try:
                                topic_extractor = LDATopicExtractor(cluster)
                                topic_str = user_util.get_topics(topic_extractor.extract_topic())
                                print '\t\t cluster_topic: %s' % topic_str
                                self.__notify__(entity, reputation_dimension, cluster, topic_str)
                            except ValueError:
                                print '\t\t No tweet in the cluster'
                except ValueError:
                    print '\t No tweet for the entity %s' % entity

    @staticmethod
    @transaction.atomic
    def __notify__(entity, reputation_dimension, tweets_in_cluster, topic_str):
        # Construct a message
        message = Message(entity=entity, reputation_dimension=reputation_dimension, topic_str=topic_str)
        # Message must be saved before associating tweets to it
        message.save()
        for tweet in tweets_in_cluster:
            message.tweet.add(tweet)

        # For each user that is interested in the entity, add the message to their message set
        ue_pairs = UserEntity.objects.filter(entity=entity)
        for ue_pair in ue_pairs:
            um_pair = UserMessage.objects.create(user=ue_pair.user)
            um_pair.save()
            um_pair.message.add(message)

if __name__ == '__main__':
    monitor = ReputationMonitor()
    monitor.scan()
