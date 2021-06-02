FROM python:3
WORKDIR /deploy/
COPY . /deploy/
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["python", "app.py"]
