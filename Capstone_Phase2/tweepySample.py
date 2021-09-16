import tweepy
# from textblob import TextBlob
import dataset 
import settings
# from sqlalchemy.exc import ProgrammingError
import json
#import emoji
import sys
import re
import urllib

#db = dataset.connect("sqlite:///tweets.db")
db = dataset.connect(settings.CONNECTION_STRING)

consumerKey = 'tNR4XEQAjcNhemWhESdgJD36V'
consumerSecret = 'bpfPt6822IBvlPTG7FoZsYvHxJCGlayFq5Y9kC5q6M4MSpXldc'
accessToken = '711852590028365828-moNblbd17ILQIaRWYqm1PqfvqsBaF3d'
accessTokenSecret = 'g9zcBGTLPl8L7ZqkwxkbwlDaG7SOPUgUXgXuRFn0JBbkd'
def get_tweets(username):
          
        # Authorization to consumer key and consumer secret
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
  
        # Access to user's access key and access secret
        auth.set_access_token(accessToken, accessTokenSecret)
  
        # Calling api
        api = tweepy.API(auth)
  
        # 200 tweets to be extracted
        number_of_tweets=200
        tweets = api.user_timeline(screen_name=username, tweet_mode="extended")
  
        # Extract the urls from the tweets (top 10 for now)
        urllist = []
        flag = False
        c = 0
        for tweet in tweets:
            print("waiting....")
            print("count of tweets extracted = ", c)
            c += 1
            if c > 1:
                break
            urls = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", tweet.full_text)
            for url in urls:
                try:
                    opener = urllib.request.build_opener()
                    request = urllib.request.Request(url)
                    response = opener.open(request)
                    actual_url = response.geturl()
                    urllist.append(actual_url)
                except:
                    pass 
                    # print(url)
        #print(urllist)
        return urllist

# this function will be used for the api call in app.py for getting tweets..
def getTweetsFromUser(username, count):
        count+=2 #added 2 to make the count proper
        
        # Authorization to consumer key and consumer secret
        auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
  
        # Access to user's access key and access secret
        auth.set_access_token(accessToken, accessTokenSecret)
  
        # Calling api
        api = tweepy.API(auth)
  
        # 200 tweets to be extracted
        number_of_tweets=200
        tweets = api.user_timeline(screen_name=username, tweet_mode="extended")
  
        # Extract the urls from the tweets (top 10 for now)
        urllist = []
        flag = False
        c=0
        for tweet in tweets:
            print("waiting....")
            print("count of tweets extracted = ", c)
            c += 1
            if c > count:
                break
            urls = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", tweet.full_text)
            for url in urls:
                try:
                    opener = urllib.request.build_opener()
                    request = urllib.request.Request(url)
                    response = opener.open(request)
                    actual_url = response.geturl()
                    urllist.append(actual_url)
                except:
                    pass 
                    # print(url)
        #print(urllist)
        return urllist



