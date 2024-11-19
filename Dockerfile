FROM python:3.12
COPY . /opt
WORKDIR /opt
RUN apt-get update && apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config

RUN pip install --upgrade pip && pip install -r src/requirements.txt
ENTRYPOINT ["sh", "entrypoint.sh"]