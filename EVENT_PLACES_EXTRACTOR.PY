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


yelp_output=yelp_scrape(city_name)

with open(f"{city_name}_yelp_places_.csv", 'r') as file:
    
    csvreader = csv.reader(file)
    for row in csvreader:
        # print(len(csvreader))
        print(f"{row[0]} {row[1]} {city_name}")
        try:
                google_place_info(city_id,f"{row[0]} {row[1]}",row[2],country)
                time.sleep(100)
        except Exception as err:
                print(err)
                pass

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
     
r=re.post(url,data=json.dumps(data),headers=Headers)
if r.json()["data"][0]['placeId']:
        print(r.json())
        print("Location matched")
        insert_event(city_id,row,r.json()["data"][0]['placeId']) 
else:
        res=google_place_info(city_id,row[6],row[7],country)
        print(res)
        print("Location inserted")
        # insert_event(city_id,row,r.json()["data"][0]['placeId'])
                
                      
                        



