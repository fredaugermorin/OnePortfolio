import pandas

class Position:
    def __init__(self, _instrumentType, _quantity, _averagePrice, _currency, _ticker, _cusip="", _isin="", _sedol=""):
        self.instrumentType = _instrumentType
        self.quantity = _quantity
        self.price = _averagePrice
        self.currency = _currency
        self.ticker = _ticker
        self.cusip = _cusip
        self.isin = _isin
        self.sedol = _sedol
        self.data = []
        self.weight = 0

    def setWeight(self,_weight):
        self.weight = _weight
        
    def display(self):
        myStr = '##############\n'
        myStr = myStr + 'Ticker: '+self.ticker+'\n'+\
                'Type  : '+self.instrumentType+'\n'+\
                'Qty   : ' +str(self.quantity) + '\n'+\
                'Price : ' +str(self.price) + '\n'\
                'MktVal: ' +str(self.marketValue()) + '\n'+\
                'Ccy   : ' +self.currency +'\n'
        if self.cusip != "" and self.cusip is not None:
            myStr = myStr + 'CUSIP : ' + self.cusip+'\n'
        elif self.isin != "" and self.isin is not None:
            myStr = myStr + 'ISIN  : ' + self.isin+'\n'
        elif self.sedol !="" and self.sedol is not None:
            myStr = myStr + 'SEDOL : ' + self.sedol+'\n'

        print(myStr)

    def costValue(self):
        return float(self.quantity * self.price)

    def marketValue(self,date):
        return float(self.data.ix[date]['AdjustedClosePrice'])*self.quantity
        
    
    def getTimeSeries(self,con):
        fields = 'ValuationDate, OpenPrice, HighPrice, LowPrice, ClosePrice, AdjustedClosePrice,Volume'
        query = "Select distinct "+ fields+" from SecuritiesMaster.dailyprice where SecurityIdentifier = '" + self.ticker +\
                "' order by ValuationDate asc"
        with con.cursor()  as cursor:
            try:
                cursor.execute(query)
                self.data = pandas.DataFrame(cursor.fetchall())
                self.data=self.data.set_index('ValuationDate')
            except:
                print('Error retreiving data for: '+ self.ticker+' please make sure it is in MySQL!')
        cursor.close()
