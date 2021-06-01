import tweepy
from textblob import TextBlob
import dataset 
import settings
from sqlalchemy.exc import ProgrammingError
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
            print("count of tweets extracted = ", c+1)
            c += 1
            if c == 10:
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

        
"""
        # Empty Array
        tmp=[] 
  
        # create array of tweet information: username, 
        # tweet id, date/time, text
        tweets_for_csv = [tweet.full_text for tweet in tweets] # CSV file created 
        for j in tweets_for_csv:
            
            # Appending tweets to the empty array tmp
            tmp.append(j) 
  
        # # Printing the tweets
        print(tmp,end="\n")
"""
"""
class TwitterStreamListener(tweepy.streaming.StreamListener):
    ''' Handles data received from the stream. '''
    '''
        We want to look at how people feel about each presidential candidate. 
        This means that we want to ignore retweets. 
        Retweets show up in the stream of data from the Twitter API,
        but the same text can show up hundreds or thousands of 
        times. This will skew our results, as 
        one person’s tweet will effectively count thousands of times in our analysis. 
    '''
    def on_status(self, status):
        if status.retweeted:
            return
        description = status.user.description
        loc = status.user.location
        text = status.text
        # now remove emojis
        #text = emoji.get_emoji_regexp().sub(r'', text)
        coords = status.coordinates
        name = status.user.screen_name
        user_created = status.user.created_at
        followers = status.user.followers_count
        id_str = status.id_str
        created = status.created_at
        retweets = status.retweet_count
        bg_color = status.user.profile_background_color
        blob = TextBlob(text)
        sent = blob.sentiment
        polarity = sent.polarity
        subjectivity = sent.subjectivity
            
        if coords is not None:
            coords = json.dumps(coords)

        print("text extracted: -", text)

        table = db[settings.TABLE_NAME]
        table.insert(dict(
        user_description=description,
        user_location=loc,
        coordinates=coords,
        text=text,
        user_name=name,
        user_created=user_created,
        user_followers=followers,
        id_str=id_str,
        created=created,
        retweet_count=retweets,
        user_bg_color=bg_color,
        polarity=sent.polarity,
        subjectivity=sent.subjectivity,))


        return True

    def on_error(self, status_code):
        print('Got an error with status code: ' + str(status_code))
        return True

    def on_timeout(self):
        print('Timeout...')
        return True 

    '''We want to look at how people feel about each presidential candidate. 
    This means that we want to ignore retweets. 
    Retweets show up in the stream of data from the Twitter API,
    but the same text can show up hundreds or thousands of 
    times. This will skew our results, as 
    one person’s tweet will effectively count thousands of times in our analysis. 
    '''
listener = TwitterStreamListener()
auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
stream = tweepy.streaming.Stream(auth, listener)
stream.filter(track=settings.TRACK_TERMS, languages=["en"])
"""
#get_tweets("CNN")