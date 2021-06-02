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