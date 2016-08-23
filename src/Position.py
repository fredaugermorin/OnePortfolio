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


class Portfolio:
    def __init__(self, _portfolioId, _ptfAsOfDate, _positions=[]):
        self.id = _portfolioId
        self.date = _ptfAsOfDate
        self.positions = _positions
        self.weight = 0

    def costValue(self):
        costVal = 0
        for position in self.positions:
            costVal += position.costValue()
        return float(costVal)

    def marketValue(self):
        mktVal = 0
        for position in self.positions:
            mktVal += position.marketValue(self.date) 
        return float(mktVal)
            
    def computeWeights(self):
        mktVal = self.marketValue()
        totalWeight = 0
        for pos in self.positions:
                pos.setWeight(pos.marketValue(self.date) / mktVal)
                totalWeight += pos.weight
        self.weight = float(totalWeight)

    def PnL(self):
        pnl = [0,0]
        pnl[0] = self.marketValue() - self.costValue()
        pnl[1] = (self.marketValue() / self.costValue() - 1)*100
        return pnl
    
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
            thisPosition.getTimeSeries(con)
            self.positions.append(thisPosition)
        cursor.close()
        
    def display(self):
        myStr = '************************* Portfolio summary ****************************\n'
        myStr+= '* Portfolio ID: '+"%10s"%self.id+ '                          As of: '+self.date+ '  *\n'
        myStr+= '***************************** Positions ********************************\n'
        myStr+= '*      Identifier    | Weight | Cost Value | Market Value |     PnL $  *\n'
        myStr+= '************************************************************************\n'
        for p in self.positions:
            myStr += '* '+"%19s"%p.ticker+'|'+"%8.2f"%p.weight+'|' +"%12.2f"%p.costValue()+'|' +"%14.2f"%p.marketValue(self.date)+\
                     '|' +"%10.2f"%(p.marketValue(self.date)-float(p.costValue()))+'  *\n'
        myStr += '************************************************************************\n'
        myStr += '* '+"%19s"%('Total')+'|'+"%8.2f"%self.weight +'|' +"%12.2f"%self.costValue()+'|' +"%14.2f"%self.marketValue()
        myStr += '|'+"%10.2f"%self.PnL()[0]+'  *\n'
        myStr += '************************************************************************\n'
        print(myStr)
        
        
