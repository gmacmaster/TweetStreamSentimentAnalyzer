from tweepy.streaming import StreamListener
import json
import sys
from textblob import TextBlob
import time
from tweepy import OAuthHandler
from tweepy import Stream

# Insert twitter api keys and secrets
consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'

access_token = 'access_token'
access_token_secret = 'access_token_secret'


class MyStreamListener(StreamListener):
    def __init__(self, time_limit=60):
        self.start_time = time.time()
        self.limit = time_limit
        self.totalSentiment = 0
        self.totalSubjectivity = 0
        self.totalTweets = 0
        super(MyStreamListener, self).__init__()

    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            jsonData = json.loads(data)
            analysis = TextBlob(jsonData['text'])
            self.totalSentiment += analysis.sentiment.polarity
            self.totalSubjectivity += analysis.sentiment.subjectivity
            self.totalTweets += 1
            return True
        else:
            return False


if __name__ == '__main__':
    while True:
        print("*******************")
        print("        Menu       ")
        print("*******************")
        print("ID   Selection")
        print("1    Run Tweet Sentiment analysis")
        print("2    Exit")
        print("*******************")
        selection = input("Select a menu option id: ")
        while selection != "1" and selection != "2":
            print("*******************")
            print("        Menu       ")
            print("*******************")
            print("ID   Selection")
            print("1    Run Tweet Sentiment analysis")
            print("2    Exit")
            print("*******************")
            selection = input("Select a menu option id: ")
        if selection == "1":
            search = input("Enter search to track: ")
            searchLength = input("Enter amount of time to track (minutes): ")
            while not searchLength.isnumeric():
                searchLength = input("Enter amount of time to track (minutes): ")
            listener = MyStreamListener(60 * int(searchLength))
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            print('Listening for Tweets...')
            stream = Stream(auth, listener)
            stream.filter(track=[search])
            print('Done')
            print('*******************')
            print("Total Tweets: ", listener.totalTweets)
            print("Average sentiment: ", listener.totalSentiment / listener.totalTweets)
            print("Average subjectivity: ", listener.totalSubjectivity / listener.totalTweets)
        else:
            sys.exit()
