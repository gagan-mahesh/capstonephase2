# Capstone-Project
Performance Evaluation of Real time tweets for business analytics using AWS Sagemaker and Spark

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

## Celery
### Steps to run with messaging queue
1. make sure to have rabbitmq and celery installed
2. open a terminal and do --> rabbitmq-server
3. open another terminal, go to "Capstone_Phase2" directory and do --> celery -A app.celery worker --loglevel=info
4. [OPTIONAL] Open another terminal, go to the same directory as above and do --> celery -A app.celery flower inorder to get real time updates
about the task queue
5. Finally, open another terminal, go to the same directory and do python app.py
6. Open localhost:portnumber and go to appropriate url!
7. Open localhost:5555 to get real time updates of the queue (given by flower)