FROM python:3.6
#FROM python:3.6-slim
#FROM python:3.6-alpine

MAINTAINER Eugene Goncharov NikeLambert@gmail.com

RUN apt-get update

ADD . /home

WORKDIR /home

RUN pip install -U -r requirements.txt \
 && apt-get clean

RUN echo "Europe/Moscow" > /etc/timezone \
 && dpkg-reconfigure -f noninteractive tzdata

# signal SIGTERM
STOPSIGNAL 15

ENTRYPOINT ["python3.6"]
