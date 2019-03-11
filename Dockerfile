FROM python:3.7-alpine
EXPOSE 8000

WORKDIR /usr/src/app


RUN apk add --no-cache \
        uwsgi-python3 \
        python3

COPY . .
RUN ./setup.py install

CMD [ "uwsgi", "--socket", "0.0.0.0:8000", \
               "--uid", "uwsgi", \
               "--plugins", "python3", \
               "--protocol", "uwsgi", \
               "--wsgi", "main:application" ]
