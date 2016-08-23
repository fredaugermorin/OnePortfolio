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

    def marketValue(self):
        return self.quantity * self.price

    def getTimeSeries(self,con):
        query = "Select distinct * from SecuritiesMaster.dailyprice where SecurityIdentifier = '" + self.ticker +\
                "' order by ValuationDate asc"
        with con.cursor()  as cursor:
            try:
                cursor.execute(query)
                self.data = pandas.DataFrame(cursor.fetchall())
            except:
                print('Error retreiving data for: '+ self.ticker+' please make sure it is in MySQL!')
        cursor.close()


class Portfolio:
    def __init__(self, _portfolioId, _ptfAsOfDate, _positions=[], _weights=[]):
        self.id = _portfolioId
        self.date = _ptfAsOfDate
        self.positions = _positions
        self.weights = _weights

    def marketValue(self):
        mktVal = 0
        for position in self.positions:
            mktVal += position.marketValue()
        return mktVal

    def computeWeights(self):
        mktVal = self.marketValue()
        weights = {}
        for pos in self.positions:
            if pos.ticker not in weights.keys():    
                weights[pos.ticker] = pos.marketValue() / mktVal
            else:
                weights[pos.ticker]+= pos.marketValue() / mktVal
        self.weights = weights
    
    def makePortfolio(self,con):
        features = 'PositionType, Quantity, Price, Currency, SecurityIdentifier, CUSIP, ISIN, SEDOL'
        query = 'Select ' + features +" FROM securitiesmaster.portfolios where PortfolioCode ='" + self.id +\
                "' and PortfolioAsOfDate ='" + self.date +"'"
        with con.cursor() as cursor:
            cursor.execute(query)
            try:
                myPositions = pandas.DataFrame(cursor.fetchall())
            except:
                print('Error making portfolio, make sure it exists in MySQL')
        #Parse all dataframe rows and create position object
        for row in myPositions.itertuples():
            thisPosition= Position(row[4],row[6],row[5],row[2],row[8],row[1],row[3],row[7])
            self.positions.append(thisPosition)
        cursor.close()
        
    def display(self):
        myStr = '********* Portfolio summary *********\n'
        myStr+= '* Portfolio ID: '+self.id+ ' As of: '+self.date+ '*\n'
        myStr+='********* Positions *********\n'
        myStr+='* Identifier  |  Weight *\n'
        for p in self.weights.keys():
            myStr += '* '+p+' | '+str(self.weights[p]) +'*\n'
        print(myStr)
        
        
