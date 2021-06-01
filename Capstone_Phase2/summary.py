import sys
import json
sys.path.insert(1, '../')
from flask import Flask 
from news_demo import *
app = Flask(__name__)

@app.route("/")
def hello():
	return "<h1>Home Screen</h1>"

@app.route("/summary")
def summarized_output():
	summary = get_summary()
	summarized_output = []
	for i in summary:
		summarized_output.append(json.dumps(i))
	summarized_output = json.dumps(summarized_output)
	return summarized_output

if __name__=="__main__":
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(debug=True)
