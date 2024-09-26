FROM python:3.10

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY requirements/dev.txt .
RUN pip install --upgrade pip
RUN pip install -r dev.txt

COPY . .