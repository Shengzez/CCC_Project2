import tweepy
from tweepy import Stream
import json as js
import argparse
from datetime import datetime
# from tweetProcess import uploadImg, postRequest
import time
import nlpfortwitter
import nltk
import couchdb as cd
#nltk.download('vader_lexicon')


secure_remote_server = cd.Server('http://admin:admin@172.26.129.141:5984')
db = secure_remote_server['tweets']
# My keys and tokens
# consumer_key = 'XMmsyU6HRJ2PCXVulgjrM4WrX'
# consumer_secret = 'PEMlBYaGi9FKuCgRdodXHboeEAtGSQgajYm8leuN8P4hVb32jJ'
# access_token = '1512011770017513476-mTa2DmJ4VKTDT9T6LM4KoP4M5WEsnT'
# access_token_secret = 'W9BXmEmkZgn9BkHy3bNGvRG2tMojFeH4BId4OzMOsm56o'

consumer_key = 'j3xcYYMhls6B7IMRgChB8LxO7'
consumer_secret = '7mztn7gOqYFvONMD0s5xJDnkDlUUF5FvIbdRCfMsVEFmAouH7i'
access_token = '966805471507005440-OJGJHd3CRttaLBMM36yewboo89A6Kd3'
access_token_secret = 'qBDLFG7am4g3221GoP0CqMgOUr6WjBLPdsURTjB5u4UAr'

access = {"consumer_key": consumer_key,
          "consumer_secret": consumer_secret,
          "access_token": access_token,
          "access_secret": access_token_secret}


# Get the authentication
def getAuth(access):
    auth = tweepy.OAuthHandler(access['consumer_key'], access['consumer_secret'])
    auth.set_access_token(access['access_token'], access['access_secret'])
    return auth


def dealStream(tweetJson, dataDict):
    try:
        dataDict = {}
        dataDict["id"] = tweetJson["id_str"]
        dataDict["user"] = tweetJson["user"]["screen_name"]
        dataDict["text"] = tweetJson["text"]

        if tweetJson["created_at"] != None:
            stringTime = tweetJson["created_at"]
            dataDict["date"] = datetime.strptime(stringTime, '%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S%z')
        else:
            dataDict["date"] = ""

        dataDict["hashtags"] = []

        if tweetJson["entities"]["hashtags"] != None:

            listHashtags = tweetJson["entities"]["hashtags"]
            for hashtag in listHashtags:
                dataDict["hashtags"].append(hashtag["text"])

        elif tweetJson["extended_tweet"] != None and tweetJson["extended_tweet"]["entities"] != None and \
                tweetJson["extended_tweet"]["entities"]["hashtags"] != None:

            listHashtags = tweetJson["extended_tweet"]["entities"]["hashtags"]
            for hashtag in listHashtags:
                dataDict["hashtags"].append(hashtag["text"])

        if tweetJson["coordinates"] != None and tweetJson["coordinates"]["coordinates"] != None:
            dataDict["geo"] = tweetJson["coordinates"]["coordinates"]

        elif tweetJson["geo"] != None and tweetJson["geo"]["coordinates"] != None:
            temp = tweetJson["geo"]["coordinates"]
            if len(temp) == 2:
                dataDict["geo"] = [temp[1], temp[0]]
        else:
            dataDict["geo"] = []

        if tweetJson["place"] != None and tweetJson["place"]["bounding_box"] != None:
            dataDict["bounding_box"] = tweetJson["place"]["bounding_box"]["coordinates"]
        else:
            dataDict["bounding_box"] = []

        newJson = js.dumps(dataDict)
        if dataDict["bounding_box"]!= []:
            process_tweet = nlpfortwitter.analysistwi(dataDict)
            db.save(process_tweet)
        return dataDict
        # responseJson = postRequest(DOMAIN, API_KEY, API_PORT["upload_tweet"]["Port"], API_PORT["upload_tweet"]["Header"], newJson, "tweet", file)


    except Exception as e:

        print(e)
        print("Cannot upload a well-formatted tweet to couchDB")
        file.write(str(dataDict))
        #file.write("Cannot upload a well-formatted tweet to couchDB\n")
        time.sleep(30)


parser = argparse.ArgumentParser(description='COMP90024 Project Twitter Streamer')
# Use like:
# python arg.py -l 1234 2345 3456 4567
# parser.add_argument('-l', '--list', nargs='+', default=[141, -38, 150, -34])
parser.add_argument('-l', '--list', nargs='+', default=[144, -38.4, 145.5, -37.5])
parser.add_argument('--filename', type=str, default="streamlog.txt")
args = parser.parse_args()

file = open(args.filename, "w")


# This is a basic listener that just prints received tweets to stdout.
class TweetListener(Stream):
    #twe = []
    #limit = 1000

    def on_data(self, data):
        dataDict = {}
        tweetJson = js.loads(data)
        new_json = dealStream(tweetJson, dataDict)
        #self.twe.append(data)
        #if len(self.twe) == self.limit:
            #self.disconnect()
        #print(tweetJson)
        # need to filter out the retweets
        # if not tweetJson["text"].startswith('RT') and tweetJson["retweeted"] == False:
            # file.write(data.decode(encoding='UTF-8'))
            # file.write(str(new_json))
            # file.write("\n")
            #if tweetJson["place"] == None:
                #print("\nNO location information")

        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    # This handles Twitter authetification and the connection to Twitter Streaming API

    auth = getAuth(access)

    stream = Stream(access['consumer_key'], access['consumer_secret'], access['access_token'], access['access_secret'])
    listener = TweetListener(access['consumer_key'], access['consumer_secret'], access['access_token'],
                             access['access_secret'])

    # This line filter Twitter Streams to capture data around Victoria state
    listener.filter(locations=args.list, track=["melbourne"], languages=['en'])

    file.close()





