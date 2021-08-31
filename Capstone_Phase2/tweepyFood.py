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

c = 0
for tweet in tweepy.Cursor(api.search,q="Idli", lang="en",tweet_mode="extended").items():
	if c>10:
		break
	if 'retweeted_status' in tweet._json:
		#temp = tweet._json['retweeted_status']['full_text'].split()
		continue
	else:
		temp = tweet.full_text.split()
	#temp = tweet.full_text.split()
	res = ""
	for i in temp:
		if i[0]!='@' and i[0]!='#' and "https" not in i:
			res+=i+str(" ")
	if len(res) > 10:
		c+=1 
		print(res)
		emotions = getEmotion(res)
		different_emotions = {}
		all_emotions = [] 
		for emotion in emotions:
			if emotion not in different_emotions:
				different_emotions['title'] = emotion
				different_emotions['content'] = emotions[emotion]
			all_emotions.append(different_emotions)
			different_emotions = {}
		print(all_emotions)
		print("\n\n")
	c+=1
