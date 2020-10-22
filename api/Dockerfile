FROM python:3.7

RUN apt-get update -y && \
    apt-get install -y python-pip python3.7-dev

WORKDIR /app

COPY . ./api

RUN pip install -r ./api/requirements.txt

EXPOSE 8000

RUN ["chmod", "+x", "./api/script/start_api.sh"]
ENTRYPOINT ["./api/script/start_api.sh"]
