FROM python:3.7
MAINTAINER Tomas Peterka <tomas@vyrobenounas.cz>

ENV DJANGO_VERSION 1.10.2

WORKDIR /usr/src/app

COPY requirements* manage.py setup.py market ./
RUN pip install -r requirements.txt -r requirements.git.txt -r requirements.dev

EXPOSE 8000

ENTRYPOINT ["/usr/src/app/develop.sh"]
