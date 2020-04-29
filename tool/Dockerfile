FROM python:3.7
RUN apt-get update -y

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./ /app
WORKDIR /app

CMD python -u run.py