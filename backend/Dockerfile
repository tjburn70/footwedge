FROM python:3.6.10-stretch

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY . /app

WORKDIR /app

RUN pip install -r ./requirements.txt

RUN ["chmod", "+x", "./script/start_api.sh"]
ENTRYPOINT ["./script/start_api.sh"]
