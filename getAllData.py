# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#BULLION RATES DATA
BullionRatesCSVPath = "D:\\Python36_projects\\StateBankPakistan\\BullionData.csv"
BullionRatesDataFrame = pd.read_csv(BullionRatesCSVPath, date_parser = "Date")
BullionRatesDataFrame['Date'] = pd.to_datetime(BullionRatesDataFrame['Date'], format = '%Y-%m-%d')
#PROPERLY SET DATETIMEINDEX
BullionRatesDataFrame = BullionRatesDataFrame.set_index(pd.DatetimeIndex(BullionRatesDataFrame['Date']))
BullionRatesDataFrame = BullionRatesDataFrame.drop('Date', axis = 1)
BullionRatesDataFrame = BullionRatesDataFrame.rename(index = str, columns = {'Price/oz':'Gold Price/oz', 'Price/gm':'Gold Price/gm'})
#PLOT OF GOLD PRICE/GM OVER TIME
BullionRatesDataFrame['Gold Price/gm'].plot()




#GET INFLATION DATA
inflationCSVPath = "D:\\Python36_projects\\StateBankPakistan\\InflationData.csv"
inflationData = pd.read_csv(inflationCSVPath)
inflationData['Period'] = pd.to_datetime(inflationData['Period'], format='%b-%y')
#PROPERLY SET DATETIMEINDEX
inflationData = inflationData.set_index(pd.DatetimeIndex(inflationData['Period']))
inflationData = inflationData.drop('Period', axis = 1)
inflationData['CPI General MoM'].plot()

#GET MONTHLY INFLATION DATA (MOM)
inflationDataMonthly = inflationData[['CPI General MoM', 'CPI Food MoM', 'CPI Non-Food MoM', 'Core NFNE MoM', 'Core Trimmed MoM', 'SPI MoM', 'WPI MoM']]
inflationDataMonthly.plot()

#GET INTEREST DATA
interestCSVPath = "D:\\Python36_projects\\StateBankPakistan\\KIBORdata.csv"
interestData = pd.read_csv(interestCSVPath)
interestData['DATE'] = pd.to_datetime(interestData['DATE'], format = '%Y-%m-%d')
interestData = interestData.drop('Unnamed: 0', axis = 1)
#PROPERLY SET DATETIMEINDEX
interestData = interestData.set_index(pd.DatetimeIndex(interestData['DATE']))
interestData = interestData.drop('DATE', axis = 1)
interestData3YR = interestData['TENOR'] == "3-  Year"
interestData[interestData3YR].plot()
#interestData.groupby('TENOR').plot() #Makes a number of plots, one for each tenor period

#GDP DATA
#GDP IN BILLION USD (10**9)
GDPDataCSVPath = "D:\\Python36_projects\\StateBankPakistan\\GDPData.csv"
GDPData = pd.read_csv(GDPDataCSVPath)
GDPData['Year'] = pd.to_datetime(GDPData['Year'], format = '%Y')
GDPData['GDP'] = GDPData['GDP'] * (10**9) #Because it's not properly scaled in the file
#PROPERLY SET DATETIMEINDEX
GDPData = GDPData.set_index(pd.DatetimeIndex(GDPData['Year']))
GDPData = GDPData.drop('Year', axis = 1)
GDPData.plot()

#USD CONVERSION RATE


#PROPERTY RATES?

#DEPOSITS = DEPENDENT 
#INTEREST RATES, BULLION RATES, INFLATION RATES, = INDEPENDENT

#ALL DATA ARE TIME BASED

#MULTIPLE LINEAR REGRESSION

#MULTIDIMENSIONAL ANALYSIS USING pandas.corr()

#RESAMPLING TIME DATA

#NORMALISE DATA


