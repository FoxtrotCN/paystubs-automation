# syntax=docker/dockerfile:1

FROM python:3.9.21-alpine3.21

WORKDIR /paystubs_automation

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY data ./data

COPY . .

EXPOSE 5000

ENV FLASK_APP=app.api


CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
