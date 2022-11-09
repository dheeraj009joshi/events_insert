from datetime import datetime
from email.headerregistry import Address
from selenium import webdriver
import json
import pandas as pd
from selenium.webdriver.common.by import By
import requests as re

from function import download_image, upload_event_image_to_aws,get_details
# from google_place_info import 

def get_events(city_name):
        caps = webdriver.DesiredCapabilities.CHROME.copy()
        caps['acceptInsecureCerts'] = True
        commenturl="http://scouterdev.ap-south-1.elasticbeanstalk.com/api/v1/Comment/Insert"
        driver=webdriver.Chrome("chromedriver.exe",desired_capabilities=caps)
        driver.maximize_window()
        driver.get(f"https://www.eventbrite.com/d/ga--{city_name}/food-and-drink--events/?page=1")
        all_pages=driver.find_element(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/div/div/section[1]/footer/div/div/ul/li[2]')
        #######################################//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/div/div/section[1]/footer/div/div/ul/li[2]/span
        no_link=str(all_pages.text).split(" ")[-1]
        print(no_link)
        Titles=[]
        Dates=[]
        city=[]
        Images=[]
        Decs=[]
        placenames=[]
        PlaceType=[]
        address=[]


        for i in range(1,2):
        
                driver.get(f'https://www.eventbrite.com/d/ga--{city_name}/food-and-drink--events/?page={i}')
                all_url=driver.find_elements(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/div/div/section[1]/div[1]/section/ul/li/div/div/div[1]/div/div/div/article/div[2]/div/div/div[1]/a')
                all_urls=[]
                dates=driver.find_elements(By.XPATH,'//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/div/div/section[1]/div[1]/section/ul/li/div/div/div[1]/div/div/div/article/div[2]/div/div/div[1]/div')
                # print(dates)
                # print(all_url)
                index_date=0
                all_dates=[]
                for u in all_url:
                        all_urls.append(u.get_attribute('href'))
                        # print(dates[index_date])
                        all_dates.append(dates[index_date].text)
                        index_date+=1    # print(all_urls)
                len_date=0
                for o in all_urls:
                        city.append("Atlanta")
                        Date=all_dates[len_date]
                        try:
                                if "Today" in Date:
                                        Dates.append(Date.replace("Today at",datetime.strftime(datetime.now(),"%Y-%m-%d")))
                                        Date=Date.replace("Today at",datetime.strftime(datetime.now(),"%Y-%m-%d"))
                                        print(Date.replace("Today at",datetime.strftime(datetime.now(),"%Y-%m-%d")))
                                elif "Tomorrow" not in Date:
                                        d=Date.split(",")
                                        del d[-1]
                                        print(d)
                                        d="".join(d)+"+2022"
                                        print(d)
                                        date=datetime_object = datetime.strptime(d,'%a %b %d+%Y')
                                        Dates.append(date)
                                        Date=date
                                else:
                                        date=datetime.now()
                                        Dates.append(date)
                                        Date=date
                                
                        except:
                                date=datetime.now()
                                Dates.append(date)
                                Date=date
                                
                        len_date+=1

                        driver.get(o)
                        
                        try:
                                try:
                                        tit=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div/div[1]/div/main/div/div[2]/div/div[1]/div/div[2]/div/div[2]/h1')
                                        Title=tit.text
                                        Titles.append(tit.text)
                                        print(tit.text)
                                except:
                                        tit=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div/div[1]/div/main/div/div[1]/div[2]/div[2]/div[1]/h1')
                                        Title=tit.text
                                        Titles.append(tit.text)
                                        print(tit.text)
                        except:
                                Titles.append("")
                                Title=""
                        try:
                                try:
                                        ing=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div/div[1]/div/main/div/div[2]/div/div[1]/div/div[1]/div/picture/img')
                                        Image=ing.get_attribute("src")
                                        im=download_image(Image)
                                        upload_ing=upload_event_image_to_aws("Sample.jpg","scouter-events",f'{(tit.text).replace(","," ").replace("  "," ").replace("’","").replace("/","").replace("+","-")}_event.jpeg'.replace(" ","-").replace("--","-"))
                                        Images.append(upload_ing["url"])
                                        print(ing.get_attribute("src"))
                                        print(upload_ing["url"])
                                except:
                                        ing=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div/div[1]/div/main/div/div[1]/div[1]/div/picture/img')
                                        Image=ing.get_attribute("src")
                                        im=download_image(Image)
                                        upload_ing=upload_event_image_to_aws("Sample.jpg","scouter-events",f'{(tit.text).replace(","," ").replace("  "," ").replace("’","").replace("/","").replace("+","-")}_event.jpeg'.replace(" ","-").replace("--","-"))
                                        Images.append(upload_ing["url"])
                                        print(ing.get_attribute("src"))
                                        print(upload_ing["url"])
                        except Exception as e:
                                Images.append("")
                                print(e)
                                Image=""
                        
                        try:
                                try:
                                        loc=(driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div/div[1]/div/main/div/div[2]/div/section[1]/div/div[1]/section/div[2]').text).replace("Location","").replace("View map","")   
                                        placename=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div/div[1]/div/main/div/div[2]/div/section[1]/div/div[1]/section/div[2]/p[1]').text
                                        address.append(loc)
                                        placenames.append(placename)
                                        print(loc)
                                        print(placename)
                                except:  
                                        try:
                                                loc=(driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div/div[1]/div/main/div/div[1]/div[2]/div[2]/section/div[1]/div[2]/section[2]/div[2]/p').text)       
                                                placename=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div/div[1]/div/main/div/div[1]/div[2]/div[2]/section/div[1]/div[2]/section[2]/div[2]/p/strong').text
                                                address.append(loc)
                                                placenames.append(placename)
                                                print(loc)
                                                print(placename)
                                        
                                        except:
                                        
                                        
                                        #//*[@id="root"]/div/div/div[2]/div/div/div/div[1]/div/main/div/div[1]/div[2]/div[2]/section/div[1]/div[2]/section/div[2]/p
                                                loc=(driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div/div[1]/div/main/div/div[1]/div[2]/div[2]/section/div[1]/div[2]/section/div[2]/p').text)       
                                                placename=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div/div[1]/div/main/div/div[1]/div[2]/div[2]/section/div[1]/div[2]/section/div[2]/p/strong').text
                                                address.append(loc)
                                                placenames.append(placename)
                                                print(loc)
                                                print(placename)
                        except Exception as e:
                                address.append("Atlanta")
                                placenames.append("")
                        try:
                                try:
                                        description=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div/div[1]/div/main/div/div[2]/div/section[1]/div/div[2]').text
                                        Decs.append(f'{o} {description}')
                                except:
                                        description=driver.find_element(By.XPATH,'//*[@id="root"]/div/div/div[2]/div/div/div/div[1]/div/main/div/div[1]/div[2]/div[2]').text
                                        Decs.append(f'{o} {description}')
                        except:
                                Decs.append(f'{o}')
                        try:   
                                a=get_details((f"{placename} Atlanta") )
                                print(a['Types'])
                                placetype=a['Types']
                                PlaceType.append(placetype)
                        except:
                                PlaceType.append("night club")  #karan 
                        
        print(len(Images))
        print(len(Titles))
        print(len(placenames))
        print(len(city))
        print(len(Dates))
        print(len(Decs))
        df=pd.DataFrame({
                "eventimage": Images,
                "eventtitle":Titles,
                "placename":placenames,
                "cityname":city,
                "eventstartdate":Dates,
                "eventDescription":Decs,
                "Address":address,
                "placeType":PlaceType
        })
        df.dropna(
        axis=0,
        how='any',
        subset=None,
        inplace=True
        )
        df.drop_duplicates()
        df.to_csv("Eventbrite_scraping_EVENTS.csv",index=False)

        df2=pd.DataFrame({
        "Name":placenames,
        "Address":address,
        "PlaceType":PlaceType
        })
        df2.dropna(
        axis=0,
        how='any',
        subset=None,
        inplace=True
        )
        df2.drop_duplicates()
        df2.to_csv("Eventbrite_scraping_places.csv",index=False)














        
        
        
        
# get_events("atlanta")     
        
        
        
        
        
        
        
        
        
        