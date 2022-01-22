FROM python:3.9-alpine
MAINTAINER NijatRajab

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /news_app
WORKDIR /news_app
COPY ./news_app /news_app

RUN adduser -D --no-create-home user

USER user