FROM python:3.11.4-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add --no-cache mariadb-connector-c-dev mariadb-client build-base && \
    pip install --upgrade pip && \
    pip install mysqlclient

COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY . /usr/src/app/

ENTRYPOINT ["/bin/sh", "/usr/src/app/entrypoint.sh"]