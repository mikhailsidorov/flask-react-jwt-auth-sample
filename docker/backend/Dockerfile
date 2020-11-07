FROM alpine:3.12.1

RUN mkdir -p /app/backend
WORKDIR /app/backend
COPY ./backend/requirements /app/backend/requirements/

RUN apk update
RUN apk upgrade
RUN apk add --update python3 python3-dev py-pip
RUN apk add postgresql-client postgresql-dev 
RUN apk add build-base gettext
RUN pip install --upgrade pip
RUN pip install -r requirements/base.txt

COPY ./backend /app/backend/

RUN mkdir /app/init
COPY ./docker/init /app/init/
