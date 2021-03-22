# Analyzing Millions of NYC Parking Violations

## Description

This project is aimed to upload lots of data from the NYC Open Data Parking Violations and pushes that information into an Elasticsearch cluster provisioned via AWS by using EC2 instance. This way, the data is never “saved” into your EC2 instance but instead streamed directly to Elasticsearch.

## General Information

dataset:https://dev.socrata.com/foundry/data.cityofnewyork.us/nc67-uf89
## 

Build the docker image

'''
docker build -t bigdata1:1.0 project01/

'''
