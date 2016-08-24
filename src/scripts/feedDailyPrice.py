import data_download as dld

import numpy as np
import pandas as pd
import pymysql.cursors
import quandl as qdl
import datetime as dt
import sys, time

qdl.ApiConfig.api_key = 'ykCFLxj3ofyyn_4s3EGu'

if len(sys.argv) == 2:
    startDate = "'"+str(sys.argv[1])+"'"
    endDate = startDate
    print('Downloading data for: ' + startDate)
elif len(sys.argv) == 3:
    startDate = "'"+str(sys.argv[1])+"'"
    endDate = "'"+str(sys.argv[2])+"'"
    print('Downloading data for dates beetween: ' + startDate + ' and ' + endDate)
else:
    raise  Exception('error: Incorrect number of input, only provide startDate and endDate.')

host = 'localhost'
user = 'faugermorin'
password = 'ab1234567'
name = 'SecuritiesMaster'

con = pymysql.connect(host=host,user=user,passwd=password,db=name,cursorclass=pymysql.cursors.DictCursor)
data = dld.obtainSymbols(con)
tickers = np.asarray(data)   
test = dld.batchEODDownload(con,startDate,endDate,tickers)
con.commit()    
con.close()
