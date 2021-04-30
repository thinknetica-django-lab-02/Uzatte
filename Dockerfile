# pull official base image
FROM python:3.8.3-alpine
# set work directory
WORKDIR /usr/src/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo pkgconfig g++ jpeg-dev zlib-dev
RUN pip install --upgrade pip
RUN pip install --upgrade pip setuptools wheel
RUN pip install p5py
RUN pip install PEP517
COPY ./requirements.txt .
RUN pip install -r requirements.txt
# copy project
COPY . .