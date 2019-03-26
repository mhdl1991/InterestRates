# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 16:40:25 2019

@author: makhan.10371
"""

#Get Gold Bullion Rates from Bullion-Rates.com
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd

#USER AGENT STRING
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}

#PROXY SETTINGS
#proxy = "[redacted]"


Years = ["2015","2016","2017","2018"]
Months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
baseURL = "https://www.bullion-rates.com/gold/PKR/%s-%s-history.htm"
URLList = [baseURL%(Year,Month) for Year in Years for Month in Months]


BullionRatesData = []
BullionRatesDataFrame = pd.DataFrame()


for URL in URLList:
    try:
        #Access Bullion-rates website and pull the tables from it using BeautifulSoup
        req = Request(URL, headers = headers)
        #req.set_proxy(proxy, 'http')
        site = urlopen(req)
        print(type(site))
        raw_html = site.read()
        html = BeautifulSoup(raw_html, 'html.parser')
        table = html.find("table", attrs = {'id': 'drDGrid'})
        for row in table.findAll("tr"): 
            #go through each row in the table
            cols = row.findAll("td")
            #The cells in each row are Date, Price/oz and Price/gm
            cols = [ele.text.strip() for ele in cols]
            BullionRatesData.append([ele for ele in cols if ele]) 
        #Data rows on the table are class="DataRow"
        #Table ID is dtDGrid  
    except Exception as e:
        print(str(e))





BullionRatesDataFrame.to_csv("D:\\Python36_projects\\StateBankPakistan\\BullionData.csv", index = False)


