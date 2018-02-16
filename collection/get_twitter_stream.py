from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
import re 
import json
import datetime
import traceback
import sys 

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("outputfile", nargs='?', default="bitcoin_tweets.json")
parser.add_argument("errorfile", nargs='?', default="bitcoin_tweets_error.txt")

args = parser.parse_args()


#Variables that contains the user credentials to access Twitter API 
access_token = ...
access_token_secret = ...
consumer_key = ...
consumer_secret = ...


class Tweet:
    def __init__(self, text, sentiment_text, polarity, created_at):
        self.text = text
        self.sentiment_text = sentiment_text
        self.polarity = polarity
        self.created_at = created_at

    def __str__(self):
        return 'Sentiment: {} {} \nText: {}\nCreated_At: {}\n'.format(self.sentiment_text, self.polarity, self.text, self.created_at)

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def __init__(self):
        self.mylist = []
    def on_data(self, data):
                
        tweet = json.loads(data)
        
        try:
            if 'retweeted_status' in tweet:
            # Retweets 
                if 'extended_tweet' in tweet['retweeted_status']:
                #When extended beyond 140 Characters limit
                    tweet_text = tweet['retweeted_status']['extended_tweet']['full_text']
                else:
                    tweet_text = tweet['retweeted_status']['text']
            else:
            #Normal Tweets
                if 'extended_tweet' in tweet:
                #When extended beyond 140 Characters limit            
                    tweet_text = tweet['extended_tweet']['full_text']
                else:
                    tweet_text = tweet['text']
            
            tweet_sentiment, polarity = self.get_tweet_sentiment(tweet_text)        
            
            newTweetObj = Tweet(text=tweet_text, 
                                sentiment_text=tweet_sentiment, 
                                polarity=polarity, 
                                created_at= datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d %H:%M:%S'))
            
            with open(args.outputfile, mode='a') as file:
                file.write('{}\n'.format(json.dumps(newTweetObj.__dict__)))     

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()            
            with open(args.errorfile, mode='a') as file:
                file.write('Error: {}\n\nTweet Info: {}\n--------------------------\n'.format(repr(traceback.format_tb(exc_traceback)), tweet))            

        return True

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False
        print(status_code)
        print('-----------------')

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))

        # set sentiment
        sentiment = None 
        if analysis.sentiment.polarity > 0:
            sentiment = 'positive'
        elif analysis.sentiment.polarity == 0:
            sentiment = 'neutral'
        else:
            sentiment = 'negative'

        return sentiment, analysis.sentiment.polarity


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener, tweet_mode='extended')

    #This line filter Twitter Streams to capture data by the keywords: 'bitcoin', 'BTC', etc
    stream.filter(track=['bitcoin', 'BTC', 'Cryptocurrency'])