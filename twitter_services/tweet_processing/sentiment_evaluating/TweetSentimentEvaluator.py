import shlex
import subprocess
from TwitterRepManagement import settings


# Returns a sentiment score given a json object representing the tweet
def rate_sentiment(tweet):
    # open a subprocess using shlex to get the command line string into the correct args list format
    sentiString = tweet['text'].encode('utf-8').replace('\n', '')

    jar_location = settings.BASE_DIR + '/twitter_services/tweet_processing/sentiment_evaluating'
    args = shlex.split("java -jar %s/SentiStrengthCom.jar stdin sentidata %s/SentStrength_Data/"
                          % (jar_location, jar_location))

    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # communicate via stdin the string to be rated. Note that all spaces are replaced with +
    stdout_text, stderr_text = p.communicate(sentiString.replace(" ", "+"))
    # remove the tab spacing between the positive and negative ratings. e.g. 1    -5 -> 1-5
    stdout_text = stdout_text.rstrip().replace("\t", "")
    # print ('%s: %s') % (type(sentiString), stdout_text)

    return stdout_text