FROM python:3.6-alpine

EXPOSE 8000
RUN mkdir -p /usr/app
WORKDIR /usr/app

COPY requirements.txt /usr/app
RUN pip install -r requirements.txt

COPY . /usr/app

CMD python server.py
