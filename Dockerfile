FROM python:3.7-alpine
  
RUN apk add build-base linux-headers

RUN pip3 install flask flask_restful sqlalchemy gunicorn

WORKDIR /app
COPY main.py /app
COPY tinyurl.py /app
COPY static /app/static
COPY templates /app/templates

RUN mkdir -p /app/logs
RUN mkdir -p /app/data

VOLUME /app/logs
VOLUME /app/data
ENV PHOTODB_PORT=17120
ENV PHOTODB_DB_NAME=photo.db

ENTRYPOINT exec /bin/sh -c "gunicorn --error-logfile /app/logs/photodb_error.log \
                                     --access-logfile /app/logs/photodb_access.log \
                                     -b 0.0.0.0:$PHOTODB_PORT \
                                     main:app"
