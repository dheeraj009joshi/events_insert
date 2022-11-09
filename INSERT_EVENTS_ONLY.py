
import time
from fetch_events import get_events
from config import Base_url
from yelp import yelp_scrape
from google_place_info import google_place_info
import csv
import requests as re
import json
from event_insert_into_db import insert_event



city_name=input(" please enter city name :- ")
city_id=input(" please enter city id :- ")
country=input( " Please enter country name :- ")

get_events(city_name)  
with open(f"Eventbrite_scraping_EVENTS.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        Headers = {"Content-Type":"application/json" }
        url=f"{Base_url}/api/v1/Mobile/RequestForAPI"
        data={
    "StoredProcedureName": "API_LOAD_PLACE_Address",
    "Params1": row[6]
}
       
print(row)
print(data)
r=re.post(url,data=json.dumps(data),headers=Headers)
print(r.json())
if r.json()["data"][0]['placeId']:
        print(r.json())
        print("Location matched")
        insert_event(city_id,row,r.json()["data"][0]['placeId']) 
else:
        res=google_place_info(city_id,row[6],row[7],country)
        r=re.post(url,data=json.dumps(data),headers=Headers)
        print()
        if r.json()["data"][0]['placeId']:
                print(r.json())
                print("Location added and then matched ")
                insert_event(city_id,row,r.json()["data"][0]['placeId']) 
 



