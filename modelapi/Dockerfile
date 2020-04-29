FROM python:3.7

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt
RUN rm requirements.txt

RUN useradd -s /bin/bash wsgi_user

COPY . /app
WORKDIR /app

ENV LANG C.UTF-8

USER wsgi_user

EXPOSE 5000

# Finally, we run uWSGI with the ini file
CMD [ "uwsgi", "--ini", "app.ini" ]