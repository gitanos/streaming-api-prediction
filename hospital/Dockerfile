FROM python:3.7.4-slim-buster

COPY ./requirements.txt requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev build-essential && \
    pip install -r /requirements.txt --no-cache && \
    apt-get remove -y gcc && apt-get -y autoremove

COPY ./ /app
WORKDIR /app

#CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:8080"]
CMD python -u streamer_aiohttp.py