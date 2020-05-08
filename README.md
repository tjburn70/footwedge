Footwedge
=======================================================

Dockerized Web-App to record golf rounds, track handicap,
set golf goals, and search golf courses

## Getting Started

* Install Docker 
* Install npm
* Generate Javascript bundle
* Build Docker images
* Setup database
* Run docker-compose up


### Prerequisites
* Docker
* npm


### Setup

1) Build you Javascript bundle:
    * ```npm run build ```

2) Build the Footwedge api and client Docker images:

    api:
     * ```docker build --file Dockerfile-api --tag footwedge-api:latest . ```
    
    client:
     * ```docker build --file Dockerfile-client --tag footwedge-client:latest . ```
     
3) Initialize the Footwedge db models:

    * ```export FLASK_APP=index```
    * ```flask db upgrade```

4) Launch Containers!
    
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
