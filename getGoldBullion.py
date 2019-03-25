# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 16:40:25 2019

@author: makhan.10371
"""
#WORK IN PROGRESS

#Get Gold Bullion Rates from Bullion-Rates.com
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd

#USER AGENT STRING
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}

#PROXY SETTINGS
#proxy = "http://10.200.1.18:8080"

Years = ["2015","2016","2017","2018"]
Months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
baseURL = "https://www.bullion-rates.com/gold/PKR/%s-%s-history.htm"
URLList = [baseURL%(Year,Month) for Year in Years for Month in Months]

BullionRatesDataFrame = pd.DataFrame()

for URL in URLList:
    try:
        #Access Bullion-rates website and pull the tables from it using BeautifulSoup
        req = Request(URL, headers = headers)
        #req.set_proxy(proxy, 'http')
        site = urlopen(req)
        raw_html = site.read()
        html = BeautifulSoup(raw_html, 'html.parser')
        
        #Data rows on the table are class="DataRow"
        #Table ID is dtDGrid
        
        
    except Exception as e:
        print(str(e))





BullionRatesDataFrame.to_csv("D:\\Python36_projects\\StateBankPakistan\\BullionData.csv", index = False)


