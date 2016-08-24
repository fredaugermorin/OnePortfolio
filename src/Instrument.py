from abc import ABCMeta, abstractmethod
import pandas
class Instrument:
    __metaclass__ = ABCMeta

    @abstractmethod
    def getPrice(self,date):
        print('Je suis un instrument en date du: ' + date)
    
    
class Equity(Instrument):
    "Class that replicates an equity(stock) instrument"
    def __init__(self,_ticker, _exchange, _cusip, _currency, _timeSeries):
        self.ticker = _ticker
        self.exchange= _exchange
        self.cusip = _cusip
        self.timeSeries = _timeSeries

    def getPrice(self,date,field='AdjustedClosePrice'):
        return self.timeSeries.ix[date][field]

        
if __name__ == '__main__':
    a = pandas.DataFrame({'AdjustedClosePrice':[22]},index=['2016-08-23'])
    eq = Equity('a','a','afdaf','cad',a)
    print(eq.getPrice('2016-08-23'))
