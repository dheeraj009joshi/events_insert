import csv
import time
from tkinter import *
import tkinter.messagebox as tkMessageBox
import requests as r
import pandas as pd
from tkinter.ttk import Combobox
import numpy as np
from tkinter import filedialog as fd
import tkinter
from tkinter import Button, ttk
import csv
from itertools import product
from config import yelp_access_key
from selenium import webdriver








def yelp_scrape(city):

    with open(f"yelp_cat.csv",'r',encoding="utf8") as csv_file:
        csv_reader=csv.reader(csv_file)
        next(csv_reader, None)
        print('iiiiiiiiiiiiiiiii')
        id=[]
        alias=[]
        name=[]
        image_url=[]
        is_closed=[]
        url=[]
        review_count=[]
        rating=[]
        categories=[]
        latitude=[]
        longitude=[]
        price=[]
        address1=[]
        address2=[]
        address3=[]
        zip_code=[]
        country=[]
        state=[]
        phone=[]
        display_phone=[]
        distance=[]
        cate_gories=[]
        print(city)
        for line in csv_reader:
            print(line[0])
            Url='https://api.yelp.com/v3/businesses/search'
            key = '4oSmDspvvCPyFbvKmQonmWfk1dXeMgfMUX7Di3Vp6Hmkql0EkinEKUEVvDPQTKl_bmcJzYc_w7wEaNRlrj-_W5kaljcN-lvvJKKgPzkAmo-CPEN0iiFaikj4Tk_-YHYx'
            headers = {
                'Authorization':'Bearer %s' %key
            }

            parameterr={
                'term':line[0],
                'radius':40000 ,
                'location':city,
                'limit':50,}



            response=r.get(Url,headers=headers,params=parameterr)
            data=response
            print(data)

            address=  [city]
            offset=np.arange(0,200,50)

            tuples=list(product(address,offset))

            for adress,step in tuples:
                search_parameters={
                'term':line[0],
                'radius':40000 ,
                'location':adress, 
                'limit':50,
                'offset':step  
                }
                res=r.get(Url,headers=headers,params=search_parameters)
                ras_data=res.json()
                print(ras_data)
                for item in ras_data['businesses']:
                    print(item)
                    cate_gories.append(line[0])
                    try:
                        id.append(item['id'])
                    except:
                        id.append('none')
                    try:
                        alias.append(item['alias'])
                    except:
                        alias.append('null')
                    try:
                        print(item['name'])
                        name.append(item['name'])
                    except:
                        name.append('null')
                    try:
                        image_url.append(item['image_url'])
                    except:
                        image_url.append('null')
                    try:
                        main=item['categories']
                        maindata=[]
                        for names in main:
                            i=names['title']
                            print(f'{i}\n')
                            maindata.append(i)
                        maindata=str(maindata).replace("'","").replace("[","").replace("]","")
                        categories.append(maindata)
                            
                    except:
                        categories.append('null')
                    try:
                        is_closed.append(item['is_closed'])
                    except:
                        is_closed.append('null')
                    try:
                        url.append(item['url'])
                    except:
                        url.append('null')
                    try:
                        review_count.append(item['review_count'])
                    except:
                        review_count.append('null')
                    try:
                        rating.append(item['rating'])
                    except:
                        rating.append('null')
                    try:
                        latitude.append(item['coordinates']['latitude'])
                    except:
                        latitude.append('null')
                    try:
                        longitude.append(item['coordinates']['longitude'])
                    except:
                        longitude.append('none')
                    try:
                        price.append(item['price'])
                    except:
                        price.append('none')
                    try:
                        address1.append(item['location']['address1'])
                    except:
                        address1.append('none')
                    try:
                        address2.append(item['location']['address2'])
                    except:
                        address2.append('none')
                    try:
                        address3.append(item['location']['address3'])
                    except:
                        address3.append('none')
            
                    try:
                        zip_code.append(item['location']['zip_code'])
                    except:
                        zip_code.append('none')
                    try:
                        country.append(item['location']['country'])
                    except:
                        country.append('none')
                    try:
                        state.append(item['location']['state'])
                    except:
                        state.append('none')
                    try:
                        phone.append(item['phone'])
                    except:
                        phone.append('none')
                    try:
                        display_phone.append(item['display_phone'])
                    except:
                        display_phone.append('none')
                    try:
                        distance.append(item['distance'])
                    except:
                        distance.append('none')
                        
        


        df=pd.DataFrame({
        # "id":id,
        # "alias":alias,
        "name":name,
        # "imagr_url":image_url,
        # "url":url,
        # "review_count":review_count,
        # "rating":rating,
        # "categories":categories,
        # "latitude":latitude,
        # "longitude":longitude,
        # "price":price,
        "address1":address1,
        # "zip_code":zip_code,
        # "country":country,
        # "state":state,
        # "phone":phone,
        # "display_phone":display_phone,
        # "distance":distance,
        "cate_gories":categories

        })
        filename=f'{city}_yelp_places_.csv'
        de2=df.drop_duplicates(subset=["name","address1","cate_gories"],keep="first")
        de2.to_csv(filename,index=False)
        return filename
    
# yelp_scrape("atlanta")