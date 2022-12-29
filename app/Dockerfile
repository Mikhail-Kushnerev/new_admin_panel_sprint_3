FROM python:3.10

WORKDIR /opt/app

ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY requirements.txt requirements.txt
COPY uwsgi/uwsgi.ini uwsgi.ini

RUN  pip install --upgrade pip \
     && pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT ["sh", "docker-entrypoint.sh"]