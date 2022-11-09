import csv
import json
import requests as re
from config import Base_url
from event_insert_into_db import insert_event
from google_place_info import google_place_info
# endpoint=f"https://scotuerazuremigrations.azurewebsites.net/api/v1/Place/AddPlace"

# Headers = {"Content-Type":"application/json" }
# request_body={
#     "CityId" :"85ab5e34-3d98-406f-a8c1-77df8ed68c2c",
#     "GooglePlaceName" :"Compound 1008 Brady Ave",
#     "PlaceType":"clubs",
#     "Country":"US"
# }
# response = requests.post(endpoint, data=json.dumps(request_body),headers=Headers)
# print(response.json())

city_id=input(" please enter city id :- ")
country=input(" please enter country :- ")

# # data={
#    "filterInfo":[
#       {
#         "filterTerm":"85ab5e34-3d98-406f-a8c1-77df8ed68c2c",
#         "filterType":"EQUALS",
#         "filterBy":"cityId"
#       }
#    ]
# }


# main=re.post(f"{Base_url}/api/v1/Place/List",json=data).json()
# # print(main)
# googlePlace_and_Place_ids={}
# for i in main["data"]:
#     print(i)
#     googlePlace_and_Place_ids[i['PlaceName']]=i['PlaceId']


with open(f"Eventbrite_scraping_EVENTS.csv", 'r') as file:
    csvreader = csv.reader(file)
    
    for row in csvreader:
       print(row[6])
       Headers = {"Content-Type":"application/json" }
       url=f"{Base_url}/api/v1/Mobile/RequestForAPI"
       data={
        "StoredProcedureName": "API_LOAD_PLACE_Address",
        "Params1": row[6]
}
       print(data)
       r=re.post(url,data=json.dumps(data),headers=Headers)
       print(r.json())



#if r.json()["data"][0]['placeId']:
#       print(r.json())
#        print("Location matched")
#else:
#        res=google_place_info(city_id,row[6],row[7],country)
#        print(res)
        
        
                # insert_event(city_id,row,place_id) 
