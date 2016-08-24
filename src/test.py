import Position as p
import Portfolio as ptf

import numpy as np
import pandas as pd
import pymysql.cursors
import quandl as qdl
import datetime as dt
import time
import sys

host = 'localhost'
user = 'faugermorin'
password = 'ab1234567'
name = 'SecuritiesMaster'

con = pymysql.connect(host=host,user=user,passwd=password,db=name,cursorclass=pymysql.cursors.DictCursor)

aptf = ptf.Portfolio('Test','2016-08-22')
myPos = aptf.makePortfolio(con)
aptf.computeWeights()
aptf.display()

con.close()
