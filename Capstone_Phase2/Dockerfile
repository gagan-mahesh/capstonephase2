FROM python:3.6
RUN mkdir /myfolder
WORKDIR /myfolder
COPY ./requirements.txt /myfolder/
RUN pip install -r requirements.txt
COPY . /myfolder/
COPY ./app.py /myfolder/
# RUN pip install -r requirements.txt
EXPOSE 8000
# ENTRYPOINT ["python", "app.py"]
CMD [ "python", "app.py" ]
