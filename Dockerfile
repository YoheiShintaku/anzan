FROM python:3.7.6-slim-buster

RUN apt-get update && apt-get install -y \
    git \
    gpg \
    vim

WORKDIR /src

ADD . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
