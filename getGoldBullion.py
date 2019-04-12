# -*- coding: utf-8 -*-

#Get Gold Bullion Rates from Bullion-Rates.com
import requests
from bs4 import BeautifulSoup
import pandas as pd

Years = ["2015","2016","2017","2018"]
Months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
baseURL = "https://www.bullion-rates.com/gold/PKR/%s-%s-history.htm"
URLList = [baseURL%(Year,Month) for Year in Years for Month in Months]

BullionRatesData = []

for URL in URLList:
    try:
        #Access Bullion-rates website and pull the tables from it using BeautifulSoup
        print(URL)
        website = requests.get(URL, verify = False)
        soup = BeautifulSoup(website.text,'html.parser')
        table = soup.find("table", attrs = {'id': 'dtDGrid'})
        for row in table.find_all("tr"): 
            #go through each row in the table
            cols = row.find_all("td")
            #The cells in each row are Date, Price/oz and Price/gm
            cols = [ele.text.strip() for ele in cols]
            BullionRatesData.append([ele for ele in cols if ele]) 
        #Data rows on the table are class="DataRow"
        #Table ID is dtDGrid  
    except Exception as e:
        print(str(e))

BullionRatesData = [row for row in BullionRatesData if row]

BullionRatesDataFrame = pd.DataFrame(BullionRatesData, columns=['Date', 'Price/oz', 'Price/gm'])
#TIME TO CONVERT.
BullionRatesDataFrame['Date'] = pd.to_datetime(BullionRatesDataFrame['Date'], format = '%d/%m/%y')

BullionRatesDataFrame['Price/oz'] = BullionRatesDataFrame['Price/oz'].str.replace(',','').astype(float)
BullionRatesDataFrame['Price/gm'] = BullionRatesDataFrame['Price/gm'].str.replace(',','').astype(float)


BullionRatesDataFrame.to_csv("D:\\Python36_projects\\StateBankPakistan\\BullionData.csv", index = False)

