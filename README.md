Footwedge
=======================================================

Dockerized web app to record Record golf rounds, keep stats, and track your handicap.

## Getting Started

* Install Docker 
* Run docker-compose up
* Migrate database

### Prerequisites
* Docker

### Setup

1) From the project root execute: ```docker-compose up```, this should build the necessary images if they don't already exist and start your containers. In the future you can rebuild images by navigating to the service directory and running ``` ./script/build_image.sh```
     
2) Migrate database:

    * ```alembic upgrade head```
    
  
## Running the tests

* handicap-service 
    * unit: ``` ./script/run_unit_tests.sh```
    * integration: ```./script/run_integration_tests.sh```
        **Note**: This requires docker containers to be running locally


## Built With

* Python
* Postgres
* Redis
* Elasticsearch
* Node.js
* Flask, Flask JWT
* SQLAlchemy
* Alembic
* React, Redux, React-Router
* serverless
* AWS Lambda, SQS
