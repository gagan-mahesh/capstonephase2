CODE EXECUTION STEPS
------------------------------
1.	Cloud Execution
	a.	Install awsebcli
	b.	Create an environment in ‘aws elasticbeasntalk environment’ [ Make sure it is a multi-container docker environment]
	c.	In terminal, go to the directory containing the dockerfile.aws.json file
	d.	Type ‘eb init’ in the terminal
	i.	Select the appropriate region, environment, and select no for ‘code commit’
	e.	Run command ‘eb local run’ in the terminal
	f.	Open docker desktop. The container created by beanstalk will now be seen.
	g.	Open ‘localhost:8000/’ in the browser
	h.	For New article module, follow step 3e
2.	Docker compose execution
	a.	Download the ‘docker-compose.yaml’ file
	b.	Run command ‘docker compose up’
	c.	Open localhost:8000/ in the browser
	d.	In case of new article module, open the end point ‘localhost:8000/results’ in a new tab and wait for a while the results to be displayed. [ Follow step 3e]
3.	Local Execution (not recommended)
	a.	Install Redis-server
	b.	Install python
	c.	Open Terminal
	a.	1st tab -> run command ‘redis-server’
	b.	2nd tab -> run command ‘python worker.py’
	c.	3rd tab -> run command ‘python app.py’
	d.	Open browser and type ‘localhost:8000’ [This open the home web page]
	e.	In case of news article module, open the endpoint ‘localhost:8000/results’ in a new tab, once a news article and the max number tweets to analyze is submitted in the text box. This page will refresh every 10 seconds and an update will be seen after a few mins/secs.


----------------------------- BELOW CONTENTS ARE FOR INTERNAL USE ONLY ------------------------------

# Capstone-Project
Performance Evaluation of Real time tweets for business analytics using AWS elastic beanstalk

# instructions for predicting using the model
1.pip install tensorflow
2.pip install transformers
3.pip install sentencepiece
#DOWNLOAD LINK FOR MODEL
https://drive.google.com/drive/folders/1LzPqE5LaGSJByModbTj4RlBNDpUKfn3z?usp=sharing

# Latest
Created Dockerfile 
### To containerize the application from scratch
1. Move the AbstractiveSummarizationModel folder to the directory 'Capstone_Phase2'
2. Create a virtual env in the directory 'capstonephase2'
    a. python3 -m venv env // env is the environment name
    b. source env/bin/activate
    Note-- use 'deactivate' command to come out of the venv
3. Create requirements.txt file
4. pip freeze > requirements.txt
5. Now build the docker image by using
    docker build -t yourdockerusername/imagename .
    Note-- do not forget the full stop
6. Run the docker using the docker dashboard
7. If following this step, be sure to create a container name by going to additional options and also to give a port number of the host. Preferably port 80.
8. Once the image is running, go to localhost:80/

## REDIS
### Installation
1. brew install redis (for mac)
2. python -m pip install redis==3.4.1 rq==1.2.2
### Running the application
#### Terminal1
1. redis-server
#### Terminal2
2. python worker.py
#### Terminal3
3. python app.py
#### Browser
4. localhost:8000/summary?count=3 [this extracts top 3 tweets...] 
5. Open another tab and localhost:8000/results [Keep refreshing this page to see top 5 tweets being displayed as and when job is processed from the redis queue]


## EMOTION 
pip install emoji if not installed
download emotion_model, emotion_tokeniser folder and dense.pkl file from the google drive 
run app.py 
/emotion is the route