import Position as p

import numpy as np
import pandas as pd
import pymysql.cursors
import quandl as qdl
import datetime as dt
import time
import sys

pos = p.Position('stock',22,33.394,'CAD','YAHOO/TO_NA',_isin='564646')
pos.display()

host = 'localhost'
user = 'faugermorin'
password = 'ab1234567'
name = 'SecuritiesMaster'

con = pymysql.connect(host=host,user=user,passwd=password,db=name,cursorclass=pymysql.cursors.DictCursor)

pos.getTimeSeries(con)

print(pos.data.tail())

posit = p.Position('stock',22,33.394,'CAD','YAHOO/TO_RY',_isin='564646')
ptf = p.Portfolio('P001','2016-08-23',[pos,pos,pos,posit])
print(ptf.marketValue())

secptf = p.Portfolio('Test','2016-08-23')
myPos = secptf.makePortfolio(con)
secptf.computeWeights()
secptf.display()

con.close()
