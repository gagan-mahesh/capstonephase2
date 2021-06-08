import sys, time
import json
sys.path.insert(1, '../')
from flask import Flask,render_template, redirect, url_for
from news_demo import *
from Capstone_Phase2.tweepySample import * 
from celery import Celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'amqp://gagan:gagan123@localhost/gagan_vhost'
app.config['CELERY_RESULT_BACKEND'] = 'amqp://gagan:gagan123@localhost/gagan_vhost'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task(bind=True)
def summariseBackground(self):
	print("SUMMARISING TEXT...")
	summary = temp()
	self.update_state(state='PROGRESS', meta={'list:', summary})
	# print("TEXT SUMMARISED!!!\n\n\n")
	# print(summary, "\n\n")
	time.sleep(1)
	# j = {'list': summary}
	return {'list': summary}

@app.route("/")
def hello():
	return "<h1>Front Page with product title</h1>"

@app.route('/temp')
def temporary():
	task = summariseBackground.apply_async()
	return redirect(url_for('printHyperlinks', task_id=task.id))

# task id is required by celery inorder to update the messaging queue...
@app.route('/printHyperlinks/<task_id>')
def printHyperlinks(task_id):
	task = summariseBackground.AsyncResult(task_id)
	if task.state == 'PENDING':
		print("\n\nPENDING....\n\n")
		response = {
			'state': task.state,
			'list': None
		}
	elif task.state == 'FAILURE':
		print("\n\nFAILURE...\n\n")
		response = {
			'state': task.state,
			'list': "failure",
		}
	else:
		response = {
			'state': task.state,
			'list': task.info
		}

	return response, 200

@app.route("/summary")
def summarized_output():
	summary = get_summary()
	# summary = summariseBackground.delay()
	# print("SUMMARIZATION FINISHED...? ", summary.ready())
	# print("SUMMARIZATION RESULT ", summary.result)
	# time.sleep(3)
	# print("SUMMARIZATION FINISHED...? ", summary.ready())
	# print("SUMMARIZATION RESULT ", summary.result)
	# return "", 200
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
