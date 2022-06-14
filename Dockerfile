FROM python:3.9

ENV PYTHONBUFFERED 1

WORKDIR /pythonNikitka

ADD . /pythonNikitka

COPY ./requirements.txt /pythonNikitka/requirements.txt

RUN pip install -r requirements.txt

COPY . /pythonNikitka