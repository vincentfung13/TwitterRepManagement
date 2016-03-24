from gensim import corpora, models
from collections import defaultdict
from twitter_services.tweet_processing.normalizing import TweetNormalizer
from pprint import pprint


# The class that handles topic extracting, it takes a list of tweets as input, and returns the top topics as output
class LDATopicExtractor(object):
    # Take in the list of tweets and build a LDA model
    def __init__(self, tweets):
        texts_tokens = [TweetNormalizer.get_tokens(tweet_orm.tweet, json=True) for tweet_orm in tweets]

        # Calculate each word's frequency and use a dictionary to store them
        frequency = defaultdict(int)
        for text in texts_tokens:
            for token in text:
                frequency[token] += 1

        # A list of lists of tokens of each tweet
        texts_tokens = [[token for token in text if frequency[token] > 1] for text in texts_tokens]

        # Assign each word a unique id
        dictionary = corpora.Dictionary(texts_tokens)
        corpus = [dictionary.doc2bow(text) for text in texts_tokens]

        # Use the corpus to initialize the model
        self.lda_model = models.LdaModel(corpus, id2word=dictionary, num_topics=10)

    def extract_topic(self):
        return self.lda_model.show_topics()


if __name__ == '__main__':
    import os
    import django
    os.environ['DJANGO_SETTINGS_MODULE'] = 'TwitterRepManagement.settings'
    django.setup()

    from twitter_services.models import Tweet
    topic_extractor = LDATopicExtractor(Tweet.objects.filter(tweet__related_entity='Apple',
                                                             tweet__reputation_dimension='Products & Services'))
    pprint(topic_extractor.extract_topic())

