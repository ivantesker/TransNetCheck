FROM python:3.5-alpine

COPY requirements.txt /

RUN pip install -r /requirements.txt

RUN sudo apt-get -y update

RUN sudo apt-get -y upgrade

RUN sudo apt-get install -y sqlite3 libsqlite3-dev

COPY app/ /app

WORKDIR /app

CMD [ "./run.sh" ]
