import sys, time
import json
sys.path.insert(1, '../')
from flask import Flask, render_template, redirect, url_for, jsonify, request
from Capstone_Phase2.news_demo import *
from Capstone_Phase2.tweepySample import getTweetsFromUser

from rq import Queue
from rq.job import Job
from worker import conn

q = Queue(connection=conn)
links_global = []

app = Flask(__name__)

# redis task 
'''
Note: this function name has to be changed later to an appropriate name!
'''
def hyperlinks_util(link):
	'''
	Later The returnsummary() should be called by passing link as argument
	and then, instead of writing link to csv file...the summarised text
	should be written!!
	'''
	with open('sample.csv', mode='a') as file_:
		file_.write("{}".format(link))
		file_.write("\n")  # Next line.
	time.sleep(2)
	return 1

@app.route("/")
def hello():
	return "<h1>Front Page with product title</h1>"

# get tweets based on username/twitter account and also how many tweets
# is required, should also be specified.
@app.route("/get_tweets/<username>/<int:count>", methods=['GET'])
def getTweets(username, count):
	tweets = getTweetsFromUser(username, count)
	print("tweets extracted are ", tweets, count)
	return jsonify(tweets=tweets), 200

# for this api call.... have to pass url as /get_summary?link=[replace with some HyperLink]
@app.route("/get_summary", methods=['GET'])
def summarise_link():
	args = request.args
	link = args.get('link')
	output = returnSummary(link)
	if output != None:
		return jsonify(summary=output), 200
	else:
		return "Error in summarising link...try again later.", 500

@app.route("/summary_all")
def summarized_output():
	summary = get_summary()
	summary_json = {}
	summarized_output = []
	for i in summary.result:
		summary_json["title"] = "Short heading if possible for every news summary"
		summary_json["content"] = i
		summarized_output.append(summary_json)
		summary_json = {}
	return render_template('summary.html',summaries=summarized_output)

# call this api for summarising text
'''
	NOTE: CURRENTLY THIS API CALL IS ONLY DISPLAYING HYPERLINKS.
	THIS WILL BE CHANGED LATER...
'''
@app.route("/summary")
def summary():
	links = None 
	jobs = None
	# check if currently there are no jobs running in the queue.
	if q.started_job_registry.count == 0:
		# first clear all data in the csv file
		fileVariable = open('sample.csv', 'r+')
		fileVariable.truncate(0)
		fileVariable.close()

		links = getTweetsFromUser("CNN", 5)
		for link in links:
			jobs = add_task(link)
			print("jobs = ", jobs)
	return render_template('summary.html', jobs=jobs)

# utility function..
def add_task(link):
	from app import hyperlinks_util

	jobs = q.jobs
	if link:
		job = q.enqueue(hyperlinks_util, link)
		jobs = q.jobs
	return jobs

# this api call is used to check if a job has been completed....
# this api call is only for debugging purposes
@app.route("/final/<jobkey>")
def final(jobkey):
	job = Job.fetch(jobkey, connection=conn)
	if job.is_finished:
		return str(job.result), 200
	return 'nay', 202

# use this api call to see links/summaries display
@app.route("/result")
def result():
	import csv
	links = []
	with open('sample.csv', 'r') as file:
		reader = csv.reader(file)
		for row in reader:
			links.append(row)
	if links == []:
		return "nan", 202
	return jsonify(links=links), 200

if __name__=="__main__":
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(host='0.0.0.0', port=8000, debug=True)
