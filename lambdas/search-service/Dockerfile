FROM python:3.7

WORKDIR /app
EXPOSE 8001

RUN apt-get update -y && \
    apt-get install -y python-pip python3.7-dev

COPY . ./
RUN pip install -r ./requirements.txt

ENTRYPOINT ["python3", "api.py"]
