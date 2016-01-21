import io
import json
import DjangoSetup
from TwitterRepManagement import settings
from twitter_services.models import TweetTrainingSet
from twitter_services.tweet_processing.sentiment_evaluating import TweetSentimentEvaluator

# This script is used to populate the database to start with.
duplicates = set()


def check_for_existence(tweet_id, tweet_dict):
    if tweet_id in tweet_dict:
            duplicates.add(tweet_id)
            return True
    else:
        return False

tweets_json = {}
ids = set()

with io.open(settings.BASE_DIR + '/twitter_services/static/Tweets/pre.3ent.json', 'r',
             encoding='utf-8') as all_tweets:
    for tweet_str in all_tweets:
        tweet_json = json.loads(tweet_str)
        tweet_id = tweet_json.get('id_str')
        sentiment_score = TweetSentimentEvaluator.rate_sentiment(tweet_str)
        tweet_json['sentiment_score'] = sentiment_score

        if not check_for_existence(tweet_id, tweets_json):
            tweets_json[tweet_id] = json.dumps(tweet_json)
            ids.add(tweet_id)

# This function is hard-coded to retrieve information for pre.3en.gold file
with io.open(settings.BASE_DIR + '/twitter_services/static/Tweets/pre.3ent.gold', 'r',
             encoding='utf-8') as classification_results:
    for line in classification_results:
        tweet_id = line[17:35]
        reputation_dimension = line[38:len(line) - 2]

        if tweet_id in ids:
            tweet = json.loads(tweets_json.get(tweet_id))
            tweet['reputation_dimension'] = reputation_dimension
            tweets_json[tweet_id] = json.dumps(tweet)

# # Insert to tweet and training set table
for id_str, tweet_json in tweets_json.iteritems():
    TweetTrainingSet.objects.create(tweet_id=id_str, tweet_json=tweet_json).save()

print 'Completed populating the training set database'



