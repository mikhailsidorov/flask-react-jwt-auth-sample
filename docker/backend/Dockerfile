FROM alpine

RUN mkdir -p /app/backend
WORKDIR /app/backend
COPY ./backend/requirements.txt /app/backend

RUN apk update
RUN apk upgrade
RUN apk add --update python3 python3-dev 
RUN apk add postgresql-client postgresql-dev 
RUN apk add build-base gettext
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./backend /app/backend/

RUN mkdir /app/init
COPY ./docker/init /app/init/
