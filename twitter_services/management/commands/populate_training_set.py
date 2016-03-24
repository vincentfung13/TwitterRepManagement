from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def __init__(self):
        self.duplicates = set()
        self.tweets_json = {}
        self.ids = set()

    def handle(self, **options):
        import io
        import json
        from TwitterRepManagement import settings
        from twitter_services.models import TweetTrainingSet

        if len(TweetTrainingSet.objects.all()[:1]) > 0:
            print 'INFO: Training set table is already populated'
            return

        with io.open(settings.BASE_DIR + '/resources/twitter_services/pre.3ent.json', 'r',
                     encoding='utf-8') as all_tweets:
            for tweet_str in all_tweets:
                tweet_json = json.loads(tweet_str)
                tweet_id = tweet_json.get('id_str')

        if not self.__check_for_existence__(tweet_id, self.tweets_json):
            self.tweets_json[tweet_id] = tweet_json
            self.ids.add(tweet_id)

        # This is hard-coded to retrieve information for pre.3en.gold file
        with io.open(settings.BASE_DIR + '/resources/twitter_services/pre.3ent.gold', 'r',
                     encoding='utf-8') as classification_results:
            for line in classification_results:
                tweet_id = line[17:35]
                reputation_dimension = line[38:len(line) - 2]

                if tweet_id in self.ids:
                    tweet = self.tweets_json.get(tweet_id)
                    tweet['reputation_dimension'] = reputation_dimension
                    self.tweets_json[tweet_id] = tweet

        # # Insert to the training set table
        for id_str, tweet_json in self.tweets_json.iteritems():
            TweetTrainingSet.objects.create(tweet=tweet_json).save()
        print 'INFO: Training set table populated.'

    def __check_for_existence__(self, tweet_id, tweet_dict):
        if tweet_id in tweet_dict:
                self.duplicates.add(tweet_id)
                return True
        else:
            return False
