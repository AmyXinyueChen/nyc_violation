# Analyzing Millions of NYC Parking Violations

## Description

This project is aimed to upload lots of data from the NYC Open Data Parking Violations and pushes that information into an Elasticsearch cluster provisioned via AWS by using EC2 instance. This way, the data is never “saved” into your EC2 instance but instead streamed directly to Elasticsearch.

## General Information

Dataset: https://dev.socrata.com/foundry/data.cityofnewyork.us/nc67-uf89

Python library: 
-sodapy==2.1.0: https://pypi.org/project/sodapy/
-requests==2.25.1 :https://pypi.org/project/requests/
-argparse: https://docs.python.org/3/library/argparse.html

## Usage

Create a docker image

```
docker build -t bigdata1:1.0 project01/
```

Go to the project01/
```
cd project01
```
Run the Docker image  
```
docker run \
 -v ${PWD}:/app \
 -e DATASET_ID=nc67-uf89  \
 -e APP_TOKEN=Your_app_token\
 -e ES_HOST=Your_ES_HOST \
 -e ES_USERNAME=Your_username \
 -e ES_PASSWORD=Your_password \
 bigdata1:1.0 --page_size=2 --num_pages=10
```
