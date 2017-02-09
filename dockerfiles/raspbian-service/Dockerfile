FROM rpi-python35

MAINTAINER Eugene Goncharov NikeLambert@gmail.com

RUN apt-get update \
 && apt-get install python3-lxml \
                    python3-pip \
                    libxml2-dev \
                    libxslt1-dev \
                    zlib1g-dev

RUN pip3 install -U pip \
                    bs4 \
                    pymongo \
                    flask \
                    lxml

RUN apt-get clean

RUN echo "Europe/Moscow" > /etc/timezone \
 && dpkg-reconfigure -f noninteractive tzdata

# signal SIGTERM
STOPSIGNAL 15

ENTRYPOINT ["python3.5"]
