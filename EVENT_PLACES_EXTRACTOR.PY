import time
from drop_duplicate import select_file
from fetch_events import get_events
from config import Base_url
from google_place_details_file import get_data_info
from yelp import yelp_scrape
from google_place_info import get_data
import csv
import requests as re
import json
from event_insert_into_db import insert_event

# 8081550724
with open(f"cities.csv", 'r',encoding="utf-8") as file:
    csvreader = csv.reader(file)
    next(csvreader)
    for row in csvreader:
        city_name=row[1]
        city_id=row[0]
        country=row[2]
        yelp_output=yelp_scrape(city_name)

        with open(yelp_output, 'r',encoding="utf-8") as file:
            csvreader = csv.reader(file)
            a=1
            next(csvreader)
            for row in csvreader:
                print(f"{row[0]} {row[1]} {city_name}")
                try:
                        print(f" Adding Place for {city_name} .....[{a}]")
                        get_data(row[0]+" "+row[1],city_id,country)
                        time.sleep(0.3)
                except Exception as err:
                        print(err)
                        print(err)
                        message_add_place={
                            "In":"Add Place",
                            "GooglePlaceName":f"{row[0]} {row[1]} ",
                            "Err message":err
                        }
                        f=open("errpe.txt","a")
                        try:
                            f.write(f"{str(message_add_place)},\n")
                        except:
                            message_add_place_={
                            "In":"Add Place",
                            "GooglePlaceName":f"",
                            "place_index":a,
                        }
                            f.write(f"{str(message_add_place_)},\n")
                        pass
                a=a+1  
     
        # get_events(city_name)  
        # select_file()
        # with open(f"Eventbrite_scraping_EVENTS_no_duplicates.csv", 'r',encoding="utf-8") as file:
        #     csvreader = csv.reader(file)
        #     next(csvreader)
        #     for row in csvreader:
        #         Headers = {"Content-Type":"application/json" }
        #         url=f"{Base_url}/api/v1/Mobile/RequestForAPI"
        #         try:
        #                 try:
        #                         print("")
        #                         print("in try ")
        #                         print("")
        #                         res=get_data(row[2]+" "+row[6],city_id,country)
        #                         print("res 1 ")
        #                         # print(res)
        #                         print("")
        #                         out=insert_event(city_id,row,res['result'])
        #                         print(out)
        #                 except: 
        #                         print("in except ")
        #                         a=get_data_info(row[2]+" "+row[6],city_id,country)
        #                         print("S")
        #                         data={
        #                 "StoredProcedureName": "API_LOAD_PLACE_Address",
        #                 "Params1": a['Address']
        #                                 }
        #                         r=re.post(url,data=json.dumps(data),headers=Headers)
        #                         print("")
        #                         print("res 2 ")
        #                         print(r.json())
        #                         insert_event(city_id,row,r.json()["data"][0]['placeId']) 
        #         except Exception as err:
        #                 print(err)
                    



