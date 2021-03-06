import luigi
import time
import requests
import os
import zipfile
from urllib.request import urlopen
from bs4 import BeautifulSoup
from zipfile import ZipFile
from io import BytesIO
import shutil
import pandas as pd
import urllib.request
from lxml import html
import gzip
import io
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import csv


		
class ConcatenateData(luigi.Task):

	def run(self):		
		cur_path = '/Users/madhu/Documents/NEU/Fall 2017/ADS Class/Final project/Data'
		d1 = pd.read_csv(cur_path+'/Data2017/On_Time_On_Time_Performance_2017_1.csv', low_memory=False)
		d2 = pd.read_csv(cur_path+'/Data2017/On_Time_On_Time_Performance_2017_2.csv', low_memory=False)
		d3 = pd.read_csv(cur_path+'/Data2017/On_Time_On_Time_Performance_2017_3.csv', low_memory=False)
		d4 = pd.read_csv(cur_path+'/Data2017/On_Time_On_Time_Performance_2017_4.csv', low_memory=False)
		d5 = pd.read_csv(cur_path+'/Data2017/On_Time_On_Time_Performance_2017_5.csv', low_memory=False)
		d6 = pd.read_csv(cur_path+'/Data2017/On_Time_On_Time_Performance_2017_6.csv', low_memory=False)
		d7 = pd.read_csv(cur_path+'/Data2017/On_Time_On_Time_Performance_2017_7.csv', low_memory=False)
		d8 = pd.read_csv(cur_path+'/Data2017/On_Time_On_Time_Performance_2017_8.csv', low_memory=False)
		d9 = pd.read_csv(cur_path+'/Data2017/On_Time_On_Time_Performance_2017_9.csv', low_memory=False)
		frame2017 = pd.concat([d1, d2, d3, d4, d5, d6, d7, d8, d9])
		frame2017.to_csv(self.output().path(), index=False)

	def output(self):
		return luigi.LocalTarget('Data2017_Uncleaned.csv')

class CombineWeatherData(luigi.Task):

	def requires(self):
		yield ConcatenateData()
	def run(self):		
		missing_data1 = df1.isnull().sum().to_frame(name='Missing_Count').reset_index()
		missing_data1['Missing_percent'] = (missing_data1['Missing_Count']/df1.shape[0])*100
		missing_data1 = missing_data1.sort_values(by='Missing_percent', axis=0, ascending=True)
		features1 = missing_data1['index'][(missing_data1.Missing_percent<99.38)]

		d = df1[features1]
		d1['Flight_Status'] = 0
		d1.loc[d1.DepDel15==1.0 ,'Flight_Status'] = 1
		d1.loc[d1.ArrDel15==1.0,'Flight_Status'] = 1
		d1.loc[d1.Cancelled==1.0, ['Flight_Status']] = 1
		d1['Flight_Status'] = d1['Flight_Status'].astype(int)
		d1['Status'] = np.where(d1['Flight_Status']==1,'Delayed', 'On Time')
		cols = features1.tolist()
		p = ['FlightDate','TailNum','Carrier','OriginAirportSeqID','OriginCityMarketID','OriginStateFips','OriginState','OriginWac','DestAirportSeqID','DestCityMArketID','DestStateFips','DestWac','DepDelay','DepDel15','DepTimeBlk','SecurityDelay','LateAircraftDelay', 'WeatherDelay', 'CarrierDelay', 'NASDelay',
			'ArrDelay','ArrDel15','ArrTimeBlk','Diverted','Flights','AirTime','DistanceGroup','CancellationCode']
		for i in p:
			if i in cols:
				cols.remove(i)
		dt1= d1[cols]
		dd.to_csv(self.output().path(), index=False)
		dt1 = dt1[dt1['Cancelled']!=1]
		del dt1["Cancelled"]
		dt1 = dt1[dt1['ArrTime'].notnull() & dt1['ArrDelayMinutes'].notnull() & dt1['ActualElapsedTime'].notnull() & dt1['ArrDelayMinutes'].notnull()]
		d1 = dt1
		d1 = d1[d1.DepDelayMinutes<1500]
		d1 = d1[d1.ArrDelayMinutes<1500]
		d1 = d1.drop((d1.Month==9) & (d1.ArrDelayMinutes>1300))
		d1.to_csv(self.output().path(), index=False)
		
	def output(self):
		return luigi.LocalTarget('Data2017_Cleaned.csv')
		
if __name__ == '__main__':
	luigi.run()