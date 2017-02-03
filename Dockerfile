FROM python:3.5.2
#FROM python:3.5.2-slim
#FROM python:3.5.2-alpine

MAINTAINER Eugene Goncharov NikeLambert@gmail.com

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
                   && pip3 install --upgrade pip \
                                             bs4 \
                                             pymongo \
                                             flask \
                                             lxml \
                   && apt-get clean

RUN echo "Europe/Moscow" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata
# signal SIGTERM
STOPSIGNAL 15

ENTRYPOINT ["python3.5"]
