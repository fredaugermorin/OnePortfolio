# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 14:01:00 2016

@author: FRED
"""

''' 
Cunducts dowload for for prices on all securities in the database.
Contains a function that executes batch downloads and one that executes
single date downloads in order to be run everyday to keep the MySQL database 
up to date
'''
import numpy as np
import pandas as pd
import pymysql.cursors
import quandl as qdl
import datetime as dt
import time
import sys

def obtainSymbols(con):
    with con.cursor() as cursor:
        myQuery = "Select distinct QuandlSymbol from quandltickers"
        cursor.execute(myQuery)
        data = pd.DataFrame(cursor.fetchall())
        return data

def batchEODDownload(con,startDate,endDate,tickerList,db='YAHOO',Provider='Quandl'):
    for ticker in tickerList:
        ticker = ticker[0]
        print('Uploading Data for: '+ticker+'...')
        with con.cursor() as cursor:
            try:
                myData = qdl.get(ticker,start_date=startDate,end_date=endDate)
            
                for row in myData.itertuples():
                    now = dt.datetime.now()
                    fields = " (ParentVendor,Vendor,SecurityIdentifier,ValuationDate, \
                         UploadDate,OpenPrice,HighPrice,LowPrice, \
                         ClosePrice,AdjustedClosePrice,Volume) "
                    query = 'insert into securitiesmaster.dailyprice' + fields +'values(' + \
                            "'" +Provider+"','" +db+"','" +ticker+"','"+ str(row[0]) + "','" +str(now)+"',"+ \
                            str(row[1])+','+str(row[2])+','+str(row[3])+','+str(row[4])+','+str(row[6])+',' \
                            +str(row[5]) +')'
                
                    cursor.execute(query)
            except:
                print('WARNING: Unable to load data for: '+ticker+ '!!')
    return 0       

    
    
