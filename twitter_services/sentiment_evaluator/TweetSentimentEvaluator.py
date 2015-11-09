import json
import shlex
import os
import subprocess

def rate_sentiment(tweet):
    # open a subprocess using shlex to get the command line string into the correct args list format
    sentiString = json.loads(tweet)['text'].encode('ascii', 'ignore')

    p = subprocess.\
        Popen(shlex.split("java -jar SentiStrengthCom.jar stdin sentidata %s/SentStrength_Data/" % (os.getcwd())),
                         stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # communicate via stdin the string to be rated. Note that all spaces are replaced with +
    stdout_text, stderr_text = p.communicate(sentiString.replace(" ","+"))
    # remove the tab spacing between the positive and negative ratings. e.g. 1    -5 -> 1-5
    stdout_text = stdout_text.rstrip().replace("\t","")
    return stdout_text

