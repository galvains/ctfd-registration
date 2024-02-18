FROM python:3.12.2

COPY core /core
WORKDIR /core

RUN apt-get update && apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config

RUN pip install --upgrade pip && pip install -r /core/requirements.txt
COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]