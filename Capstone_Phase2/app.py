import sys, time
import json
sys.path.insert(1, '../')
from flask import Flask, render_template, redirect, url_for, jsonify, request
from Capstone_Phase2.news_demo import *
from Capstone_Phase2.tweepySample import getTweetsFromUser
from Capstone_Phase2.emotion import *
#from Capstone_Phase2.forms import *
from rq import Queue
from rq.job import Job
from worker import conn

q = Queue(connection=conn)
links_global = []

app = Flask(__name__)

# # redis task 
# '''
# Note: this function name has to be changed later to an appropriate name!
# '''	
def summary_util(link):
	'''
	Later The returnsummary() should be called by passing link as argument
	and then, instead of writing link to csv file...the summarised text
	should be written!!
	'''
	summ = returnSummary(link)
	with open('sample.csv', mode='a') as file_:
		file_.write("{}".format(summ))
		file_.write("\n")  # Next line.
	time.sleep(2)
	return 1

@app.route("/")
def Front_page():
	return render_template('frontpage.html')

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

# temp = [{
# 		'title' : "Jello world",
# 		'content': "Hello world",
# 		},
# 		{
# 		'title' : "kello world",
# 		'content' :"mello world",
# 		}
# 		]

@app.route("/summary_all",methods=['GET','POST'])
def summarized_output():
	if request.method=='POST':
		username = request.form.get('username')
		num_of_tweets = request.form.get('Number of tweets')
		print(username,num_of_tweets)
	summary = get_summary()
	#summary = temp.copy()
	summary_json = {}
	summarized_output = []
	for i in summary:
		summary_json["content"] = i
		summarized_output.append(summary_json)
		summary_json = {}
	return render_template('summary.html',summaries=summarized_output)
# # # call this api for summarising text
# # '''
# # 	NOTE: CURRENTLY THIS API CALL IS ONLY DISPLAYING HYPERLINKS.
# # 	THIS WILL BE CHANGED LATER...
# # # '''
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
			links = getTweetsFromUser(username, num_of_tweets)
			for link in links:
				#akash's function by passing link, username
				jobs = add_task(link)
				print("jobs = ", jobs)
		return "Summarising....", 202
	except Exception as e:
		return "Something went wrong, try again in a while! ", 500

# # # # utility function..
def add_task(link):
	from app import summary_util

	jobs = q.jobs
	if link:
		job = q.enqueue(summary_util, link)
		jobs = q.jobs
	return jobs

# # # # # this api call is used to check if a job has been completed....
# # # # # this api call is only for debugging purposes
@app.route("/final/<jobkey>")
def final(jobkey):
	job = Job.fetch(jobkey, connection=conn)
	if job.is_finished:
		return str(job.result), 200
	return 'nay', 202

# # # # # # use this api call to see links/summaries display
@app.route("/result")
def result():
	import csv
	summaries = []
	with open('sample.csv', 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			summaries.append(row[0])
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


# #emotion detection 
@app.route('/emotion',methods=['POST','GET'])
def emotion_detection():
	summary = request.get_json()
	#summary = "migrant is body hanging out of plane on runway of casablanca is mohammed v airport . authorities believe it is most likely that the man died during take off in conakry passengers said they were shocked to find out what happened during the flight . sadly, this is not the first time a stowaway has made their way onto a plane . earlier this year the body of a suspected plane landed just three feet away from a sunbathing resident in clapham . the sunbather is in his 20s and is still waiting for it . it is believed to have fallen from the plane on the runway in morocco . one of the passengers said: i am very sad for him and his family . police have released horrifying footage shows the unidentified man was killed during take-off in london after trying to leave the"
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

@app.route('/input',methods=['POST','GET'])
def input_form():
	return render_template('input_form.html')


if __name__=="__main__":
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(host='0.0.0.0', port=8000, debug=True)
