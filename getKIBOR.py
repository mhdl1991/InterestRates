# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 19:08:00 2019

@author: makhan.10371
"""
#IMPORT PACKAGES
from urllib.request import urlopen, Request
import re, glob, os, tabula
import pandas as pd
from datetime import datetime as dt
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

#USER AGENT STRING
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}

#PROXY SETTINGS
#proxy = "[redacted]"

#MONTHS AND YEARS
years = ["2018","2017","2016","2015"]#["2018","2017","2016","2015","2014","2013","2012"]
months = ["Dec","Nov","Oct","Sep","Aug","Jul","Jun","May","Apr","Mar","Feb","Jan"]

#DOWNLOAD DAILY KIBOR RATES FOR EVERY DAY OF EVERY MONTH OF THE SELECTED RANGE OF YEARS
PDFs_List = []
for year in years:
    for month in months:
        URL ="http://www.sbp.org.pk/ecodata/kibor/" + year + "/" + month + "/index.asp"
        print(URL)
        try:
            req = Request(URL, headers = headers)
            #req.set_proxy(proxy, 'http')
            site = urlopen(req)
            #Use BeautifulSoup?
            raw_html = site.read()
            html = BeautifulSoup(raw_html, 'html.parser')
            for a in html.select('a'):
                download_URL = ""
                #If the link is a download link for a PDF
                if re.match(r"kibor-\d\d-[a-z][a-z][a-z]-\d\d\.pdf",a['href'],flags=re.IGNORECASE):
                    download_URL = "http://www.sbp.org.pk/ecodata/kibor/" + year +"/" + month + "/" + str(a['href'])
                    print(download_URL)
                elif re.match(r"http://www\.sbp\.org\.pk/ecodata/kibor/\d\d\d\d/[a-z][a-z][a-z]/kibor-\d\d-[a-z][a-z][a-z]-\d\d\.pdf", a['href'],flags=re.IGNORECASE):
                    #ummmmm
                    download_URL = str(a['href'])
                    print(download_URL)
                if download_URL:
                    PDFs_List.append(download_URL)

        except Exception as e:
            print(str(e))

#SAVE THE LIST OF URLS FOR LATER 
if PDFs_List:
    with open('C:\\StateBankPakistanProject\\PDFdumpFolder\\pdf_list.txt','w') as f:
        for item in PDFs_List:
            f.write("{}\n".format(item))

#DOWNLOAD EVERYTHNG IN THE LIST:
PDFdumpPath = "C:\\StateBankPakistanProject\\PDFdumpFolder\\"
if PDFs_List:
    for URL in PDFs_List:
        print(URL)
        try:
            req = Request(URL, headers = headers)
            #req.set_proxy(proxy, 'http')
            file = urlopen(req)
            file = file.read()
            filename = PDFdumpPath + URL.split('/')[-1]
            with open(filename,'wb') as f:
                f.write(file)

        except Exception as e:
            print(str(e))

#ONCE YOU HAVE ALL THE PDFS AND HAVE DOWNLOADED THEM IT'S TIME TO PROCESS THEM
#ALL FILENAMES ARE IN THE FORM Kibor-DD-MMM-YY.pdf 
#USE STRING SPLITTING STUFF TO EXTRACT THE DATE FROM THAT FILENAME

#MAKE A DATAFRAME? COLUMNS ARE TENOR, BID, OFFER, DATE
KIBORdf = pd.DataFrame()            
os.chdir(PDFdumpPath)
fileList = glob.glob("*.pdf")
for file in fileList:
    fileDate = file[6:-4]     
    getData = tabula.read_pdf(file)
    date= dt.strptime(fileDate,"%d-%b-%y").date()
    getData["DATE"] = date
    KIBORdf = KIBORdf.append(getData)

KIBORdf = KIBORdf.sort_values(by='DATE') 
KIBORdf = KIBORdf.reset_index()
KIBORdf = KIBORdf.drop("index", axis = 1)
KIBORdf.rename(columns = {"Tenor":"TENOR"}, inplace = True)
KIBORdf.to_csv("C:\\StateBankPakistanProject\\DatadumpFolder\\KIBORdata.csv")



#Try making a chart?
KIBOR_1yr = KIBORdf['TENOR'] == '1 - Year'
OneYear = KIBORdf[KIBOR_1yr]

ax = plt.gca()
OneYear.plot(kind='line',x='DATE',y='BID', ax = ax)
OneYear.plot(kind='line',x='DATE',y='OFFER', ax = ax)
plt.show()
