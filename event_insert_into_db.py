
import requests as re
from config import Base_url


def insert_event(city_id,record,place_id):
    try:
        url=f"{Base_url}/api/v1/Event/Insert"
        data={
            "CityId": city_id,
            "PlaceId": place_id,
            "EventTitle":record[1] ,
            "EventDescription": record[5],
            "EventDate": record[4],
            "MigratedImage": record[0],
            "Hide": False
        }
        res = re.post(url, json=data,verify=False)
        print(data)
        print('time', 'message',  'inserted event :- ' + res.text)
    except Exception as err:
        print(err)
    