FROM python:3.7
COPY . .
RUN apt-get update
RUN apt-get install redis-server -y
RUN pip install -r requirements.txt
EXPOSE 50051
CMD rq worker --with-scheduler & redis-server --port 6379 & python3 -u server.py
