FROM python:2.7
MAINTAINER Michał Papierski <michal@papierski.net>

ADD . /code
WORKDIR /code
ENTRYPOINT ["./app.py"]
