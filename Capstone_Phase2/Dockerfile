FROM python:3.8
RUN mkdir /myfolder
WORKDIR /myfolder
COPY ./requirements.txt /myfolder/
# RUN pip install -r requirements.txt
RUN pip install numpy
RUN pip install pandas
RUN pip install tensorflow==2.7.0
RUN pip install flask
RUN pip install flask-restful
RUN pip install transformers
RUN pip install newspaper3k
RUN pip install redis
RUN pip install redis-server
RUN pip install tweepy
RUN pip install rq
RUN pip install dataset
RUN pip install sentencepiece
RUN pip install emoji
RUN pip install demoji
RUN pip install scipy
RUN pip install -U scikit-learn
COPY . /myfolder/
COPY ./app.py /myfolder/
# RUN pip install -r requirements.txt
EXPOSE 8000
# ENTRYPOINT ["python", "app.py"]
CMD [ "python", "app.py" ]
