import sys, time
import json
sys.path.insert(1, '../')
from flask import Flask, render_template, redirect, url_for, jsonify, request
from Capstone_Phase2.news_demo import *
from Capstone_Phase2.tweepySample import getTweetsFromUser
from Capstone_Phase2.emotion import *
from Capstone_Phase2.tweepyFood import *
from rq import Queue
from rq.job import Job
from worker import conn

q = Queue(connection=conn)
links_global = []

app = Flask(__name__)



@app.route("/")
def Front_page():
	return render_template('frontpage.html')

# '''
# Input forms 
# '''
@app.route('/input',methods=['POST','GET'])
def input_form():
	return render_template('input_form.html')

@app.route('/input_food',methods=['POST','GET'])
def input_form_food():
	return render_template('input_form_food.html')

# # redis task 
# '''
# Note: this function name has to be changed later to an appropriate name!
# '''	
def summary_util(t):
	'''
	Later The returnsummary() should be called by passing link as argument
	and then, instead of writing link to csv file...the summarised text
	should be written!!
	'''
	article = get_article(t[0], t[1])
	# article = get_article("https://edition.cnn.com/2021/07/06/asia/hong-kong-alleged-plot-intl-hnk/index.html?utm_source=twCNN&utm_term=link&utm_content=2021-07-06T05%3A45%3A45&utm_medium=social", t[1])
	summ = returnSummary(article)
	with open('sample.csv', mode='a+') as file_:
		file_.write("{}".format(summ))
		file_.write("\n")  # Next line.
	time.sleep(2)
	return 1

# get tweets based on username/twitter account and also how many tweets
# # is required, should also be specified.
@app.route("/get_tweets/<username>/<int:count>", methods=['GET'])
def getTweets(username, count):
	tweets = getTweetsFromUser(username, count)
	print("tweets extracted are ", tweets, count)
	return jsonify(tweets=tweets), 200

# # # # # for this api call.... have to pass url as /get_summary?link=[replace with some HyperLink]
@app.route("/get_summary", methods=['GET'])
def summarise_link():
	args = request.args
	link = args.get('link')
	output = returnSummary(link)
	if output != None:
		return jsonify(summary=output), 200
	else:
		return "Error in summarising link...try again later.", 500

@app.route("/summary_all",methods=['GET','POST'])
def summarized_output():
	if request.method=='POST':
		username = request.form.get('username')
		num_of_tweets = request.form.get('Number of tweets')
		#print(username,num_of_tweets)
	summary = get_summary()
	#summary = temp.copy()
	summary_json = {}
	summarized_output = []
	for i in summary:
		summary_json["content"] = i
		summarized_output.append(summary_json)
		summary_json = {}
	return render_template('summary.html',summaries=summarized_output)

# # # # utility function..
def add_task(link, username):
	from app import summary_util

	jobs = q.jobs
	if link:
		job = q.enqueue(summary_util, (link, username))
		jobs = q.jobs
	return jobs

# # # # # # this api call is used to check if a job has been completed....
# # # # # # this api call is only for debugging purposes
@app.route("/final/<jobkey>")
def final(jobkey):
	job = Job.fetch(jobkey, connection=conn)
	if job.is_finished:
		return str(job.result), 200
	return 'nay', 202

# # # # # # # use this api call to see links/summaries display
@app.route("/result")
def result():
	import csv
	summaries = []
	with open('sample.csv', 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			
			summaries.append(" ".join(row))
	
	summarized_output = []
	if summaries == []:
		# return "nan", 202
		return render_template('summary.html',summaries=summarized_output), 200
	d = {}	# dictionary to store in json format and passing to the html page...
	for i in summaries:
		d["content"] = i
		summarized_output.append(d)
		d = {}
	# return jsonify(summaries=summarized_output), 200
	return render_template('summary.html',summaries=summarized_output), 200


# # # # call this api for summarising text
# # # '''
# # # 	NOTE: CURRENTLY THIS API CALL IS ONLY DISPLAYING HYPERLINKS.
# # # 	THIS WILL BE CHANGED LATER...
# # # # '''
@app.route("/summary", methods=['GET','POST'])
def summary():
	links = None 
	jobs = None
	username = ""
	num_of_tweets = 0
	if request.method=='POST':
		username = request.form.get('username')
		num_of_tweets = request.form.get('Number of tweets')
		num_of_tweets = int(num_of_tweets)
		#print(username,num_of_tweets)
	# check if currently there are no jobs running in the queue.
	try:
		if q.started_job_registry.count == 0:
			# first clear all data in the csv file
			fileVariable = open('sample.csv', 'r+')
			fileVariable.truncate(0)
			fileVariable.close()

			#count = int(request.args.get('count'))
			print("username = ", username)
			links = getTweetsFromUser(username, num_of_tweets)
			for link in links:
				#akash's function by passing link, username
				jobs = add_task(link, username)
				print("jobs = ", jobs)
		# return "Summarising....", 202
		return render_template('buffer.html'), 202
	except Exception as e:
		return "Something went wrong, try again in a while! ", 500


# #emotion detection 
@app.route('/emotion',methods=['POST','GET'])
def emotion_detection():
	summary = request.form['temp']
	emotions = getEmotion(summary)
	different_emotions = {}
	all_emotions = [] 
	for emotion in emotions:
		if emotion not in different_emotions:
			different_emotions['title'] = emotion
			different_emotions['content'] = emotions[emotion]
		all_emotions.append(different_emotions)
		different_emotions = {}
	return render_template('emotion.html',summaries = all_emotions), 200


@app.route("/review", methods=['GET','POST'])
def review():
	HashTag = ""
	num_of_tweets = 0
	if request.method=='POST':
		HashTag = request.form.get('HashTag')
		num_of_tweets = request.form.get('Number of tweets')
		num_of_tweets = int(num_of_tweets)
	all_reviews = get_reviews(HashTag,num_of_tweets)
	print(all_reviews)
	reviews_json = []
	d = {}	# dictionary to store in json format and passing to the html page...
	for i in all_reviews:
		d["content"] = i
		reviews_json.append(d)
		d = {}
	return render_template('reviews.html',reviews=reviews_json), 200


if __name__=="__main__":
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(host='0.0.0.0', port=8000, debug=True)
