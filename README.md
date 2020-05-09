Footwedge
=======================================================

Dockerized Web-App to record golf rounds, track handicap,
set golf goals, and search golf courses

## Getting Started

* Install Docker 
* Build Docker images
* Setup database
* Run docker-compose up


### Prerequisites
* Docker


### Setup


1) Build the Footwedge api and client Docker images:

    api:
     * ```docker build --file Dockerfile-api --tag footwedge-api:latest . ```
    
    client:
     * ```docker build --file Dockerfile-client --tag footwedge-client:latest . ```
     
2) Initialize the Footwedge db models:

    * ```export FLASK_APP=index```
    * ```flask db upgrade```

3) Launch Containers!
    
    * ```docker-compose up```
    
  
## Running the tests

* TBD


## Built With

* Python
* Postgres
* Redis
* Elasticsearch
* Node.js
* Flask, Flask JWT, Flask SQLAlchemy, Flask Migrate
* React, Redux, React-Router


## Features To Come
* Book tee-times
* Mobile client!
