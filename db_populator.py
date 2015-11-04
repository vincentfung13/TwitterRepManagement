import json
import psycopg2
import sys
import os

# This script is used to pupulate the database to start with.

duplicates = set()


def check_for_existence(tweet_id, tweet_list):
    for tweet in tweet_list:
        if tweet['id'] == tweet_id:
            duplicates.add(tweet_id)
            return True
    return False

tweets_json = []
ids = set()

with open(os.getcwd() + '/Tweets/pre.3ent.json', 'r') as all_tweets:
    for tweet_str in all_tweets:
        tweet = {}
        tweet_json = json.loads(tweet_str)
        tweet['id'] = tweet_json.get('id_str')
        tweet['tweet_json'] = tweet_str
        if not check_for_existence(tweet['id'], tweets_json):
            tweets_json.append(tweet)
            ids.add(tweet['id'])

pre3en_golden = []
with open(os.getcwd() + '/Tweets/pre.3ent.gold', 'r') as classification_results:
    for line in classification_results:
        tweet = {}
        tweet['entity_id'] = line[1:14]
        tweet['id'] = line[17:35]
        tweet['dimension'] = line[38:len(line) - 2]
        if tweet['id'] in ids:
            pre3en_golden.append(tweet)

if len(sys.argv) != 4:
    print len(sys.argv)
    print 'Usage: python db_populator.py db_name user password'
    exit()

# Connect to the database
conn = psycopg2.connect('dbname=%s user=%s password=%s' % (sys.argv[1], sys.argv[2], sys.argv[3]))
cur = conn.cursor()

# # Insert to tweet and training set table
i = 0
for tweet_json in tweets_json:
    i += 1
    if i <= 1000:
        cur.execute("INSERT INTO twitter_services_tweet_training VALUES (%s, %s);",
                    (tweet_json['id'], tweet_json['tweet_json']))
    cur.execute("INSERT INTO twitter_services_tweet VALUES (%s, %s);",
                (tweet_json['id'], tweet_json['tweet_json']))
conn.commit()

# Insert to dimension table
for item in pre3en_golden:
    cur.execute("INSERT INTO twitter_services_tweet_reputation_dimension VALUES (%s, %s, %s, %s);",
                ("%s: %s" % (item['id'], item['entity_id']), item['entity_id'], item['dimension'], item['id']))

print 'Committing changes and closing connection'
conn.commit()
cur.close()
conn.close()



