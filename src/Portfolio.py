import Position,pandas

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
                raise ValueError('Could not create portfolio, make sure the name and date exist in SQL!')
        #Parse all dataframe rows and create position object
        for row in myPositions.itertuples():
            thisPosition= Position.Position(row[4],row[6],row[5],row[2],row[8],row[1],row[3],row[7])
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
