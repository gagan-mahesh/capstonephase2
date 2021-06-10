import sys, time
import json
sys.path.insert(1, '../')
from flask import Flask, render_template, redirect, url_for, jsonify, request
from Capstone_Phase2.news_demo import *
from Capstone_Phase2.tweepySample import getTweetsFromUser

app = Flask(__name__)

@app.route("/")
def hello():
	return "<h1>Front Page with product title</h1>"

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

@app.route("/summary")
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

if __name__=="__main__":
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(host='0.0.0.0', port=8000, debug=True)
