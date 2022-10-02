import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import numpy as np 
import pandas as pd 
import time


import streamlit as st 

def wuzzuf(link):
    
    result = requests.get(link)
    src= result.content
    soup = BeautifulSoup(src,"lxml")
    job_titles = soup.find_all("h2",{"class":"css-m604qf"})
    company_names = soup.find_all("a",{"class":"css-17s97q8"})
    location_names = soup.find_all("span",{"class":"css-5wys0k"})
    job_skills = soup.find_all("a",{"class":"css-5x9pm1"})
    job_types = soup.findAll("span",{"class":"css-1ve4b75 eoyjyou0"})
    posts_time_n = soup.findAll("div",{"class":"css-do6t5g"})
    posts_time_o = soup.findAll("div",{"class":"css-4c4ojb"})
    posts_time =  [*posts_time_n , *posts_time_o]
    job_title=[]
    company_name=[]
    location_name=[]
    skills = []
    links = []
    responsipilities = []
    job_type = []
    post_time = []
    logo=[]
    for i in range (len(job_titles)):
        job_title.append(job_titles[i].text)
        links.append("https://wuzzuf.net/"+job_titles[i].find("a").attrs["href"])
        company_name.append(company_names[i].text.replace("-"," "))
        location_name.append(location_names[i].text)
        skills.append(job_skills[i].text.replace("."," "))
        job_type.append(job_types[i].text)
        post_time.append(posts_time[i].text)
    
    for link in links :
        try :
            result2 = requests.get(link,timeout=5)
            src2= result2.content
            soup2 = BeautifulSoup(src2,"lxml")

            requirements = soup2.find("span",{"itemprop":"responsibilities"}).text.replace("\u202f"," ").strip()
            logo.append(soup2.find_all('meta',{'property':"og:image"})[0]['content'])
            responsipilities.append(requirements)
            print ("job switched")
            time.sleep(1)
        except Exception as e :
            print (str(e))
    file_list=[job_title,company_name,location_name,skills,links,job_type,post_time,responsipilities , logo]
    exported=zip_longest(*file_list) #to make unpacking
    with open ("C:/Users/user/Desktop/scrap_data3.csv",'w',encoding="utf-8") as myfile:
        wr=csv.writer(myfile)
        wr.writerow(["Job Title","Company Name","Location Name","Skills","Links","Job Type","Post Time","responsipilities","Logo"])
        wr.writerows(exported)
    data = pd.read_csv('C:/Users/user/Desktop/scrap_data3.csv')
    return data

def convert_df(df):
    return df.to_csv(index=False, encoding='utf-8')

W_link=st.text_input('Enter link')
scrap_button=st.button('Scrap')


if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame()

st.dataframe(st.session_state.df)


st.download_button(
        "Download CSV file",
        convert_df(st.session_state.df),
        "Jobs.csv",
        "text/csv",
        key='download-csv'
)

if scrap_button==True :
    st.session_state.df=wuzzuf(W_link)

    