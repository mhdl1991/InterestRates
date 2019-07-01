# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 12:27:59 2019

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
proxy = "[redacted]"

#MONTHS AND YEARS
years = ["2018","2017","2016"] #["2018","2017","2016","2015","2014","2013","2012"]
months = ["Dec","Nov","Oct","Sep","Aug","Jul","Jun","May","Apr","Mar","Feb","Jan"]

#DOWNLOAD DAILY DAILY WEIGHTED AVERAGE RATES FOR EVERY DAY OF EVERY MONTH OF THE SELECTED RANGE OF YEARS
PDFs_List = []
for year in years:
    for month in months:
        URL ="http://www.sbp.org.pk/ecodata/rates/war/" + year + "/" + month + "/" + month + ".asp"
        print(URL)
        try:
            req = Request(URL, headers = headers)
            req.set_proxy(proxy, 'http')
            site = urlopen(req)
            #Use BeautifulSoup?
            raw_html = site.read()
            html = BeautifulSoup(raw_html, 'html.parser')
            for a in html.select('a'):
                download_URL = ""
                #If the link is a download link for a PDF
                if re.match(r"\d\d-[a-z][a-z][a-z]-(\d\d|\d\d\d\d)\.pdf",a['href'],flags=re.IGNORECASE) :
                    download_URL = "http://www.sbp.org.pk/ecodata/rates/war/" + year +"/" + month + "/" + str(a['href'])
                    print(download_URL)
                elif re.match(r"http://www\.sbp\.org\.pk/ecodata/rates/war/\d\d\d\d/[a-z][a-z][a-z]/\d\d-[a-z][a-z][a-z]-(\d\d|\d\d\d\d)\.pdf", a['href'],flags=re.IGNORECASE):
                    #ummmmm
                    download_URL = str(a['href'])
                    print(download_URL)
                if download_URL:
                    PDFs_List.append(download_URL)
                     
        except Exception as e:
            print(str(e))
    
#SAVE THE LIST OF URLS FOR LATER 
if PDFs_List:
    with open('pdf_list.txt','w') as f:
        for item in PDFs_List:
            f.write("{}\n".format(item))

#DOWNLOAD EVERYTHNG IN THE LIST:
PDFdumpPath = "D:\\Python36_projects\\StateBankPakistan\\DWARPDFdumpFolder\\"
if PDFs_List:
    for URL in PDFs_List:
        print(URL)
        try:
            req = Request(URL, headers = headers)
            req.set_proxy(proxy, 'http')
            file = urlopen(req)
            file = file.read()
            filename = PDFdumpPath + URL.split('/')[-1]
            with open(filename,'wb') as f:
                f.write(file)
            
        except Exception as e:
            print(str(e))
            
#ONCE YOU HAVE ALL THE PDFS AND HAVE DOWNLOADED THEM IT'S TIME TO PROCESS THEM
#ALL FILENAMES ARE IN THE FORM DD-MMM-YY.pdf 
#USE STRING SPLITTING STUFF TO EXTRACT THE DATE FROM THAT FILENAME

def parseDate(text):
    for fmt in ('%d-%b-%y', '%d-%b-%Y'):
        try:
            return dt.strptime(text, fmt).date()
        except ValueError:
            pass
    raise ValueError('no valid date format found')

#MAKE A DATAFRAME, COLUMNS ARE CURRENCY, BUYING, SELLING
DWARdf = pd.DataFrame()            
os.chdir(PDFdumpPath)
fileList = glob.glob("*.pdf")
for file in fileList:
    fileDate = file[:-4]     
    getData = tabula.read_pdf(file)
    date= parseDate(fileDate)
    getData["DATE"] = date
    DWARdf = DWARdf.append(getData)

DWARdf = DWARdf.sort_values(by='DATE') 
DWARdf = DWARdf.reset_index()
DWARdf = DWARdf.drop("index", axis = 1)
DWARdf.to_csv("D:\\Python36_projects\\StateBankPakistan\\DWARdata.csv", index = False)



#MAYBE ADD A STEP HERE TO LOAD FROM CSV?
DWARdf = pd.read_csv("D:\\Python36_projects\\StateBankPakistan\\DWARdata.csv",date_parser = "DATE")
DWARdf['DATE'] = pd.to_datetime(DWARdf['DATE'], format = '%Y-%m-%d')
DWARdf.index = DWARdf['DATE']
DWARdf = DWARdf.drop('DATE', axis = 1)
