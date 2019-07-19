# -*- coding: utf-8 -*-
#IMPORT NEEDED LIBRARIES
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn import preprocessing

#DO RENAMING OF COLUMNS BEFORE DATETIME INDEX
#BULLION RATES DATA
BullionRatesCSVPath = "D:\\Python36_projects\\StateBankPakistan\\BullionData.csv"
BullionRatesDataFrame = pd.read_csv(BullionRatesCSVPath, date_parser = "Date")
BullionRatesDataFrame['Date'] = pd.to_datetime(BullionRatesDataFrame['Date'], format = '%Y-%m-%d')
#PROPERLY SET DATETIMEINDEX
BullionRatesDataFrame = BullionRatesDataFrame.rename(columns = {'Price/oz':'Gold Price/oz', 'Price/gm':'Gold Price/gm'})
BullionRatesDataFrame = BullionRatesDataFrame.set_index(pd.DatetimeIndex(BullionRatesDataFrame['Date']))
BullionRatesDataFrame = BullionRatesDataFrame.drop('Date', axis = 1)
#PLOT OF GOLD PRICE/GM OVER TIME
BullionRatesMonthAverage = BullionRatesDataFrame.resample('M').mean()
#BullionRatesMonthAverage['Gold Price/gm'].plot()

#GET INFLATION DATA
inflationCSVPath = "D:\\Python36_projects\\StateBankPakistan\\InflationData.csv"
inflationData = pd.read_csv(inflationCSVPath)
inflationData['Period'] = pd.to_datetime(inflationData['Period'], format='%d-%b-%y')
#PROPERLY SET DATETIMEINDEX
inflationData = inflationData.set_index(pd.DatetimeIndex(inflationData['Period']))
inflationData = inflationData.drop('Period', axis = 1)
#inflationData['CPI General MoM'].plot()

#GET MONTHLY INFLATION DATA (MOM)
inflationDataMonthly = inflationData[['CPI General MoM', 'CPI Food MoM', 'CPI Non-Food MoM', 'Core NFNE MoM', 'Core Trimmed MoM', 'SPI MoM', 'WPI MoM']]
#inflationDataMonthly.plot()

#GET INTEREST/KIBOR DATA
interestCSVPath = "D:\\Python36_projects\\StateBankPakistan\\KIBORdata.csv"
interestData = pd.read_csv(interestCSVPath)
interestData['DATE'] = pd.to_datetime(interestData['DATE'], format = '%Y-%m-%d')
interestData = interestData.drop('Unnamed: 0', axis = 1)
#PROPERLY SET DATETIMEINDEX
interestData = interestData.set_index(pd.DatetimeIndex(interestData['DATE']))
interestData = interestData.drop('DATE', axis = 1)
interestData3YR = interestData['TENOR'] == "3-  Year"
interestData3YR = interestData3YR.rename(columns = {'BID':'KIBOR BID', 'OFFER': 'KIBOR OFFER'})
#interestData[interestData3YR].plot()
#interestData.groupby('TENOR').plot() #Makes a number of plots, one for each tenor period
#MONTHLY 3-YEAR INTEREST RATES (BASED ON MEAN OF DAILY INTEREST RATES FOR THAT MONTH)
#interestDataMonthly = interestData[interestData3YR].resample('M').mean()
interestDataMonthly = interestData[interestData3YR].resample('M').mean()
#interestDataMonthly.plot()

#GDP DATA
GDPDataCSVPath = "D:\\Python36_projects\\StateBankPakistan\\GDPData.csv"
GDPData = pd.read_csv(GDPDataCSVPath)
GDPData['Year'] = pd.to_datetime(GDPData['Year'], format = '%Y')
#PROPERLY SET DATETIMEINDEX
GDPData = GDPData.set_index(pd.DatetimeIndex(GDPData['Year']))
GDPData = GDPData.drop('Year', axis = 1)
#MONTHLY GDPDATA
GDPMonthlyData = GDPData.resample('M').pad()
#GDPMonthlyData.plot()

#KSE100 DATA
#KSE DATA TAKEN FROM https://markets.businessinsider.com/index/historical-prices/kse_100/1.1.2015_31.12.2018
KSE100DataCSVPath = "D:\\Python36_projects\\StateBankPakistan\\kse100.csv"
KSE100Data = pd.read_csv(KSE100DataCSVPath)
#PROPERLY SET DATETIMEINDEX
KSE100Data = KSE100Data.set_index(pd.DatetimeIndex(KSE100Data['DATE']))
KSE100Data = KSE100Data.drop('DATE', axis = 1)
KSE100Data = KSE100Data.rename(columns = {'CLOSING PRICE':'KSE CLOSING', 'OPEN':'KSE OPEN', 'DAILY HIGH':'KSE DAILY HIGH', 'DAILY LOW':'KSE DAILY LOW'})
#MONTHLY KSE100
KSE100MonthlyData = KSE100Data.resample('M').pad()

#CRUDE OIL PRICES

#DUBAI CRUDE

#BRITISH BRENT

#US WTI

#USD CONVERSION RATE
#Taken from State Bank Pakistan site
DWARDataCSVPath = "D:\\Python36_projects\\StateBankPakistan\\DWARdata.csv"
DWARData = pd.read_csv(DWARDataCSVPath)
#PROPERLY SET DATETIMEINDEX
DWARData = DWARData.set_index(pd.DatetimeIndex(DWARData['DATE']))
DWARData = DWARData.drop('DATE', axis = 1)
#MONTHLY USDdataRate
USDData = DWARData[DWARData['CURRENCY'] == "USD"]
USDData = USDData.drop('CURRENCY', axis = 1)
USDData['BUYING'] = USDData['BUYING'].str.replace(" ","")
USDData['SELLING'] = USDData['SELLING'].str.replace(" ","")
USDData = USDData.rename(columns = {'BUYING':'USD BUYING', 'SELLING':'USD SELLING'})
#USDMonthlyData = USDData.astype(float).resample('M').mean()
USDMonthlyData = USDData.astype(float).resample('M').pad() #Got something missing?

#COLLATE ALL THE DATA INTO ONE 
dataFramesList = [GDPMonthlyData, interestDataMonthly, inflationDataMonthly, BullionRatesMonthAverage, KSE100MonthlyData, USDMonthlyData]
combinedData = pd.concat(dataFramesList,axis = 1)  

combinedData_interpolated = combinedData.interpolate()

#Save the combined DataFrame as a CSV for now
combinedData.to_csv("D:\\Python36_projects\\StateBankPakistan\\AllData.csv", index = False)


#FEATURE SCALING?
scaler = preprocessing.StandardScaler()
combinedData_interpolated[combinedData_interpolated.columns] = scaler.fit_transform(combinedData_interpolated[combinedData_interpolated.columns])


#MAKE A HEATMAP
corr = combinedData_interpolated.corr()
sns.heatmap(corr, xticklabels=corr.columns, yticklabels=corr.columns)
'''
This part is seemingly unaffected by the addition of feature scaling
'''

'''
Denote some features as X and one feature as y
#Somehow the Dollar price and Gold price are most correlated to KIBOR 
X = combinedData_interpolated["USD BUYING", "Gold Price/gm"]
y = combinedData_interpolated["KIBOR OFFER"]
'''


