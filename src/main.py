import os
import sys
import argparse
import requests

from requests.auth import HTTPBasicAuth

from sodapy import Socrata







DATASET_ID =os.environ.get("DATASET_ID")
APP_TOKEN = os.environ.get("APP_TOKEN") 
ES_HOST = os.environ.get("ES_HOST") 
ES_USERNAME = os.environ.get("ES_USERNAME")
ES_PASSWORD = os.environ.get("ES_PASSWORD") 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process data from violation')
    parser.add_argument('--page_size',  type=int,
                        help='how many rows to get per page')
    parser.add_argument('--num_pages', type=int,
                        help='how many pages to get in total',required=True)
    args = parser.parse_args(sys.argv[1:])
    
    try:
        limit = int(args.page_size)
    except:
        limit=1000
    print(limit)

    client = Socrata(
        "data.cityofnewyork.us",
        APP_TOKEN,
    )

  
    # STEP 1: try to create an index in elasticsearch
    try:
        resp = requests.put(
            f"{ES_HOST}/viola", 
            auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD),
            json= {
                      "settings": {
                        "number_of_shards": 1
                      },
                      "mappings": {
                        "properties": {
                             'plate': { "type": "keyword" },
                             'state': { "type": "keyword" },
                             'license_type': { "type": "keyword" },
                             'summons_number': { "type": "float" },
                             'issue_date': { "type": "date","format": "mm/dd/yyyy"},
                             'violation_time': { "type": "keyword" },
                             'violation': { "type": "keyword" },
                             'judgment_entry_date': { "type": "keyword" },
                             'fine_amount': { "type": "float" },
                             'penalty_amount': { "type": "float" },
                             'interest_amount': { "type": "float" },
                             'reduction_amount': { "type": "float" },
                             'payment_amount': { "type": "float" },
                             'amount_due': { "type": "float" },
                             'precinct': { "type": "keyword" },
                             'county': { "type": "keyword" },
                             'issuing_agency': { "type": "keyword" },
                             'violation_status': { "type": "keyword" },
                        }
                      }
                    },
        )
        resp.raise_for_status()        
    except Exception as e:
        print("Index already exists! skipping")
        print(f"{e}")
        
    # STEP 2: query the data and get rows
    for i in range(args.num_pages):
        print('page:',i+1)
        rows = client.get(DATASET_ID, limit=limit, offset=i*limit, order=":id")
        # STEP 3: convert the row data into the correct types as needed.
        for row in rows:
            try:
    
                fieldlists=['summons_number','fine_amount','penalty_amount','interest_amount','reduction_amount','payment_amount','amount_due']
                for key in list(row.keys()):
                    if key in fieldlists:
                        row[key]=float(row[key])
                        
            except Exception as e:
                print(f"SKIPPING! Failed to transform row: {row}. Reason: {e}")
                continue
            
            # STEP: POST this data to elasticsearch

            try:
                resp = requests.post(
                    f"{ES_HOST}/viola/_doc", 
                    auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD),
                    json=row,
                )
                print(resp)
                print(resp.json())
                resp.raise_for_status()

              
            except Exception as e:
                print(f"Failed to create document: {e}")
    
