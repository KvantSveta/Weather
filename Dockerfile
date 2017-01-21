FROM python:3.5.2

MAINTAINER Eugene Goncharov NikeLambert@gmail.com

RUN apt-get update && apt-get install -y apt-utils \
                   && pip3 install --upgrade bs4 \
                                             pymongo \
                                             flask \
                                             lxml

RUN echo "Europe/Moscow" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata
# signal SIGTERM
STOPSIGNAL 15

ENTRYPOINT ["python3.5"]
