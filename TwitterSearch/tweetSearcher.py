import tweepy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import couchdb as cd
import tweetsProcess

LIMIT = 1000

secure_remote_server = cd.Server('http://admin:admin@172.26.129.141:5984')
db = secure_remote_server['mel_tweets']

consumer_key = 
consumer_secret = 
access_token = 
access_token_secret = 
bearer_token = 


# You can authenticate as your app with just your bearer token
client = tweepy.Client(bearer_token=bearer_token,wait_on_rate_limit = True)
query = 'house OR home OR apartment OR townhouse OR property OR realtor OR real estate OR foreclosures OR fsbo OR condos OR owner OR rent OR corporation OR resident OR maintenance cost OR loan OR mortgage OR hoa OR co-op fees OR utilities OR special assessments OR bill OR utility OR origin OR gas point_radius:[145.035 -37.822 25mi]'

for response in tweepy.Paginator(client.search_all_tweets,
                                 query=query, max_results = 500,
                                 tweet_fields=['created_at', 'lang', 'geo'],
                                 expansions=['author_id', 'geo.place_id'],
                                 start_time="2017-01-01T00:00:00+00:00",
                                 end_time="2022-05-01T00:00:00+00:00",
                                 limit= LIMIT):
    for item in response.data:
        document = {}
        tweet = str(item)
        processed_tweet = tweetsProcess.preprocessing(tweet)
        document["text"] = processed_tweet
        analy = TextBlob(processed_tweet)
        score = SentimentIntensityAnalyzer().polarity_scores(processed_tweet)
        neg = score['neg']
        neu = score['neu']
        pos = score['pos']
        if neg > pos:
            document["sentiment"] = ('negative')
        elif pos > neg:
            document["sentiment"] = ('positive')
        else:
            document["sentiment"] = ('neutural')
        db.save(document)
