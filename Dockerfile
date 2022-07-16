# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

RUN apk update & apk add tzdata

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]