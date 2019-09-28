FROM ubuntu:16.04

COPY requirements.txt /

RUN apt-get update                                                                                            && \
    apt-get install -y libssl-dev libvips-dev libnss3-dev dbus-x11 nautilus libxss1 dbus-user-session python3    \
                       libgconf-2-4 wget netcat apt-transport-https libgl1-mesa-dev cheese nodejs python3-pip    \
                       python3-dev

RUN pip3 install -r /requirements.txt

RUN sudo apt-get -y update

RUN sudo apt-get -y upgrade

RUN sudo apt-get install -y sqlite3 libsqlite3-dev

COPY app/ /app

WORKDIR /app

CMD [ "./run.sh" ]
