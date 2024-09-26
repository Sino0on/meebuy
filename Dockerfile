FROM python:3.11-slim

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY requirements/dev.txt .
RUN pip install --upgrade pip
RUN pip install -r dev.txt

COPY . .