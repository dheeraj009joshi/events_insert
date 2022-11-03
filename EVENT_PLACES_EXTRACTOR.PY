from yelp import yelp_scrape
from google_place_info import google_place_info
import csv
import requests as re
import json





city_name=input(" please enter city name")
city_id=input(" please enter city id")

yelp_output=yelp_scrape(city_name)

with open(f"{yelp_output}", 'r') as file:
    
    csvreader = csv.reader(file)
    for row in csvreader:
        google_place_info([0])


data={
   "filterInfo":[
      {
        "filterTerm":"85ab5e34-3d98-406f-a8c1-77df8ed68c2c",
        "filterType":"EQUALS",
        "filterBy":"cityId"
      }
   ]
}
# data={"cityId":"85ab5e34-3d98-406f-a8c1-77df8ed68c2c"}
try:
        main=re.post("http://scouterlive.ap-south-1.elasticbeanstalk.com/api/v1/Place/List",json=data).json()
except:
        main=re.post("http://scouterdev.ap-south-1.elasticbeanstalk.com/api/v1/Place/List",json=data).json()
# print(main)
googlePlace_and_Place_ids={}
for i in main["data"]:
    print(i)
    googlePlace_and_Place_ids[i['PlaceName']]=i['PlaceId']


