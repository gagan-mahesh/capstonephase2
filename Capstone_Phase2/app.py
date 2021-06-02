import sys
import json
sys.path.insert(1, '../')
from flask import Flask,render_template
from news_demo import *
app = Flask(__name__)

@app.route("/")
def hello():
	return "<h1>Front Page with product title</h1>"

@app.route("/summary")
def summarized_output():
	summary = get_summary()
	summary_json = {}
	summarized_output = []
	for i in summary:
		summary_json["title"] = "Short heading if possible for every news summary"
		summary_json["content"] = i
		summarized_output.append(summary_json)
		summary_json = {}
	return render_template('summary.html',summaries=summarized_output)

if __name__=="__main__":
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(host='0.0.0.0', port=80, debug=True)
