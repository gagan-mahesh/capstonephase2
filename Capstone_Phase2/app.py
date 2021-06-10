import sys, time
import json
sys.path.insert(1, '../')
from flask import Flask,render_template, redirect, url_for
from news_demo import *
from Capstone_Phase2.tweepySample import * 

app = Flask(__name__)

@app.route("/")
def hello():
	return "<h1>Front Page with product title</h1>"

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
