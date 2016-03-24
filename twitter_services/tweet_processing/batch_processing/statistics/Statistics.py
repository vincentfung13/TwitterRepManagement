from __future__ import division

if __name__ == '__main__':
    import os
    import django
    os.environ['DJANGO_SETTINGS_MODULE'] = 'TwitterRepManagement.settings'
    django.setup()

from twitter_services.models import Tweet
from twitter_services.tweet_processing.utility import get_negative_score, get_positive_score
import datetime


# Given a time interval, entity and dimension, it returns a dictionary of statistics.
def get_stats(time_threshold, entity, dimension=None):
    if dimension:
        senti_list = [tweet.tweet['sentiment_score']
                      for tweet in Tweet.objects.filter(tweet__related_entity=entity,
                                                        tweet__reputation_dimension=dimension,
                                                        created_at__gt=time_threshold)]
    else:
        senti_list = [tweet.tweet['sentiment_score']
                      for tweet in Tweet.objects.filter(tweet__related_entity=entity,
                                                        created_at__gt=time_threshold)]

    if len(senti_list) > 0:
        negative_scores = get_negative_score(senti_list)
        positive_scores = get_positive_score(senti_list)
        negative_count = len([score for score in negative_scores if score > 2])
        tweet_count = len(senti_list)

        # Compute simple statistics
        reputation_score = __get_reputation_score__(tweet_count, positive_scores, negative_scores)

        stat = dict()
        stat['total_tweets_count'] = tweet_count
        stat['negative_count'] = negative_count
        stat['reputation_score'] = reputation_score

        return stat
    else:
        return {
            'total_tweets_count': 0,
            'negative_count': 0,
            'reputation_score': 0
        }


def __get_reputation_score__(tweet_count, positive_scores, negative_scores):
    # Get rid of the indifferent scores
    positive_scores = [positive_score for positive_score in positive_scores if positive_score != 1]
    negative_scores = [negative_score for negative_score in negative_scores if negative_score != 1]

    score = 0
    for positive_score in positive_scores:
        score += positive_score

    for negative_score in negative_scores:
        score -= negative_score

    return score/tweet_count * 10


if __name__ == '__main__':
    import pytz
    from twitter_services.tweet_processing import utility
    from twitter_services.models import Statistics
    from django.utils import timezone

    time_threshold = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=1)
    for entity in utility.entities_list:
        statistics_dict_whole = get_stats(time_threshold, entity)
        # Statistics.objects.create(related_entity=entity,
        #                           total_tweets_count=statistics_dict_whole['total_tweets_count'],
        #                           negative_count=statistics_dict_whole['negative_count'],
        #                           reputation_score=statistics_dict_whole['reputation_score'])
        print entity
        for k, v in statistics_dict_whole.iteritems():
            print k, v
        for dimension in utility.dimension_list:
            statistics_dict_dimension = get_stats(time_threshold, entity, dimension=dimension)
            # Statistics.objects.create(related_entity=entity,
            #                           reputation_dimension=dimension,
            #                           total_tweets_count=statistics_dict_dimension['total_tweets_count'],
            #                           negative_count=statistics_dict_dimension['negative_count'],
            #                           reputation_score=statistics_dict_dimension['reputation_score'])
            print '\t' + dimension
            for k, v in statistics_dict_dimension.iteritems():
                print '\t' + k, v