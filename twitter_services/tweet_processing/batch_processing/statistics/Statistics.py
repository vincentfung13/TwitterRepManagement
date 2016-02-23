from __future__ import division
import DjangoSetup
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

    time_threshold = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=1)
    for entity in utility.entities_list:
        statistics_dict_whole = get_stats(time_threshold, entity)
        print entity
        for k, v in statistics_dict_whole.iteritems():
            print k, v
        for dimension in utility.dimension_list:
            stat_dict = get_stats(time_threshold, entity, dimension)
            print '\t' + dimension
            for k, v in stat_dict.iteritems():
                print '\t' + k, v