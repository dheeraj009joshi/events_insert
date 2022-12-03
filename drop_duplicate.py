import pandas as pd
from tkinter import filedialog as fd

def select_file():
#     global f
#     filename = fd.askopenfilename(
#         title='Open a file',
#         initialdir='/',
#         )
#     f=filename
#     print(f)
# a=select_file() 
  
    df = pd.read_csv("Eventbrite_scraping_EVENTS.csv") 
    print(df)
    df2 = df.drop_duplicates( subset=["Name","Address"],keep="first")
    print(df2)
    df2=df2.dropna(how="any")

    # print(df2)


    df2.to_csv(f'Eventbrite_scraping_EVENTS_no_duplicates.csv',index=False)
