import json
import requests

from config import Base_url

def google_place_info(CityId,placename,placetype,country):
    endpoint=f"{Base_url}/api/v1/Place/AddPlace"

    Headers = {"Content-Type":"application/json" }
    request_body={
        "CityId" :CityId,
        "GooglePlaceName" :placename,
        "PlaceType":placetype,
        "Country":country
    }
    response = requests.post(endpoint, data=json.dumps(request_body),headers=Headers)
    print(response.json())
    return response.json()
    
# google_place_info()