FROM rpi-python35

MAINTAINER Eugene Goncharov NikeLambert@gmail.com

ADD . /home

WORKDIR /home

RUN apt-get update \
 && apt-get install -y python3-lxml \
                       python3-pip \
                       libxml2-dev \
                       libxslt1-dev \
                       zlib1g-dev \
 && pip install -U -r requirements.txt \
 && apt-get clean

RUN echo "Europe/Moscow" > /etc/timezone \
 && dpkg-reconfigure -f noninteractive tzdata

# signal SIGTERM
STOPSIGNAL 15

ENTRYPOINT ["python3.5"]
