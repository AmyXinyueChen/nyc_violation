# Analyzing Millions of NYC Parking Violations

## Description

This project is aimed to upload lots of data from the NYC Open Data Parking Violations and pushes that information into an Elasticsearch cluster provisioned via AWS by using EC2 instance. This way, the data is never “saved” into your EC2 instance but instead streamed directly to Elasticsearch.

## General Information

Dataset: 
Open Parking and Camera Violations:https://dev.socrata.com/foundry/data.cityofnewyork.us/nc67-uf89

Python library: 
- sodapy==2.1.0: https://pypi.org/project/sodapy/
- requests==2.25.1 :https://pypi.org/project/requests/
- argparse: https://docs.python.org/3/library/argparse.html

NYC Open Data API app token application:
https://data.cityofnewyork.us/profile/edit/developer_settings


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
 bigdata1:1.0 --page_size=10 --num_pages=10
```
## Arguments
- --page_size: This command line argument is optional. It will ask for how many records to request from the API per call. If not provided, this value is default to 1000.
- --num_pages: You must provide num_pages to execute the whole script.

