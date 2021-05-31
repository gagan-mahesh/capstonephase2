import tweepy
import csv

consumer_key = 'tNR4XEQAjcNhemWhESdgJD36V'
consumer_secret = 'bpfPt6822IBvlPTG7FoZsYvHxJCGlayFq5Y9kC5q6M4MSpXldc'
access_token = '711852590028365828-moNblbd17ILQIaRWYqm1PqfvqsBaF3d'
access_token_secret = 'g9zcBGTLPl8L7ZqkwxkbwlDaG7SOPUgUXgXuRFn0JBbkd'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Open/Create a file to append data
csvFile = open('tweets1.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)


for tweet in tweepy.Cursor(api.search,q="Healthy Food", lang="en").items():
    print (tweet.created_at, tweet.text)
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])