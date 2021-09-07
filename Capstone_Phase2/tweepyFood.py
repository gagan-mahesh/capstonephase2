import tweepy
import csv
import sys, time
import json
sys.path.insert(1, '../')
from Capstone_Phase2.emotion import *

consumer_key = 'tNR4XEQAjcNhemWhESdgJD36V'
consumer_secret = 'bpfPt6822IBvlPTG7FoZsYvHxJCGlayFq5Y9kC5q6M4MSpXldc'
access_token = '711852590028365828-moNblbd17ILQIaRWYqm1PqfvqsBaF3d'
access_token_secret = 'g9zcBGTLPl8L7ZqkwxkbwlDaG7SOPUgUXgXuRFn0JBbkd'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def get_reviews(hashtag,num_of_tweets):
	all_reviews = []
	counter = 0
	for tweet in tweepy.Cursor(api.search,q=hashtag, lang="en",tweet_mode="extended").items():
		if counter>num_of_tweets:
			break
		if 'retweeted_status' in tweet._json:
			#tweet_res = tweet._json['retweeted_status']['full_text'].split()
			continue
		else:
			tweet_res = tweet.full_text.split()
		res = ""
		for i in tweet_res:
			if i[0]!='@' and i[0]!='#' and "https" not in i:
				res+=i+str(" ")

		if len(res) > 10:
			counter+=1 
			all_reviews.append(res)
		counter+=1
	return all_reviews
