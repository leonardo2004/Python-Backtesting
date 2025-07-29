import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt

class YFTicker():
    def __init__(self, ticker: str, start: dt.datetime, end: dt.datetime, time_interval: str):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.time_interval = time_interval

    #downloads the ticker from yfinance
    def download(self, fill_method = '', drop_na=False, drop_zero=False):
        self.data = yf.download(
            self.ticker,
            start=self.start,
            end=self.end,
            interval=self.time_interval,
            auto_adjust=True,
        multi_level_index=False
        ).loc[:,["Open","High","Low","Close","Volume"]].round(2)
    
        #fill nan values using the selected method
        if fill_method == 'ffill':
            self.data = self.data.ffill()
        elif fill_method == 'bfill':
            self.data = self.data.bfill()
        elif fill_method == 'interpolate':
            self.data = self.data.interpolate()
        
        #drop zeros
        if drop_zero:
            self.data = self.data.replace(to_replace=0,value=np.nan)

        #drop not a number values
        if drop_na:
            self.data = self.data.dropna()

    #saves ticker as .pkl file
    def save_pkl(self, path="./ticker.pkl"):
        self.data.to_pickle(path)

    #loads ticker as .pkl file
    def load_pkl(self, path="./ticker.pkl"):
        self.data = pd.read_pickle(path)
           
    #WIP -> calculates intraday_change
    def intraday_change(self):
        idchange = 100*self.data[['Open','Close']].pct_change(axis=1)
        pass

    #returns a pandas series with the logarithmic return calculated based on the closing column
    def log_creturn(self):
        return np.log(self.data.Close / self.data.Close.shift()).fillna(0)
    
    #returns a pandas series with the return calculated based on the closing column
    def creturn(self):
        return (self.data.Close - self.data.Close.shift()).fillna(0)
    
    #returns the value of a column in a specific time
    def get_value(self, time: np.datetime64, column: str)->float:
        return (self.data[column].loc[time])

class Operation():
    def __init__(self, start_price: float, start_time: np.datetime64, op_type = 'Long'):
        '''op_type: Long or Short'''
        self.op_type = op_type
        self.is_open = True

        #Price
        self.start_price = start_price
        self.end_price = None
        self.percentual_return = None
                
        #Time
        self.start_time = start_time
        self.end_time = None

    def end(self, end_price: float, end_time: np.datetime64):

        #Updating variables
        self.is_open = False
        self.end_price = end_price
        self.end_time = end_time

        if self.is_long():
            self.percentual_return = self.end_price/self.start_price
        else: 
            self.percentual_return = self.start_price/self.end_price
    
    #Checks is an operation is long
    def is_long(self) -> bool:
        if self.op_type == "Long":
            return True
        return False
    
    #Checks is an operation is short
    def is_short(self) -> bool:
        if self.op_type == "Short":
            return True
        return False

class Strategy():
    def __init__(self, signal_array: np.array, ticker: YFTicker, initial_balance: float = None,  trading_fee = 0):

        #Start values
        self.ticker = ticker
        self.balance = initial_balance if initial_balance else self.ticker.data.Close.iloc[0]
        self.trading_fees = trading_fee

        #Transform the signal array to get the difference of the values
        self.ticker.data['Signal'] = np.diff(signal_array,prepend=0)

        #Results
        self.total_fees = 0
        self.operations = []
        self.ticker.data['Buy and Hold'] = (self.ticker.data.Close / self.ticker.data.Close.iloc[0]) * self.balance
        self.ticker.data['Strategy Return'] = pd.Series()
        self.win_rate = 0

    #Calculates fee for each operation
    def calculate_fee(self) -> float:
        return (self.trading_fees/100) * self.balance

    def run(self):
        for time in self.ticker.data.index:

            close = self.ticker.get_value(time, 'Close')
            signal = self.ticker.get_value(time, 'Signal')

            #End short operation
            if (signal > 0 
                and self.operations
                and self.operations[-1].is_open
                and self.operations[-1].is_short()):
                
                #Update balance
                self.operations[-1].end(close, time)
                self.balance *= self.operations[-1].percentual_return

                #Count a win
                if self.operations[-1].percentual_return > 1:
                    self.win_rate+=1 

                #Update fees
                self.total_fees += self.calculate_fee()
                self.balance -= self.calculate_fee()
                
                signal -= 1

            #Start long operation
            elif (signal > 0 
                  and not (self.operations 
                           and self.operations[-1].is_open)):
                
                #Start operation
                self.operations.append(Operation(close,time,'Long'))

                #Update fees
                self.total_fees += self.calculate_fee()
                self.balance -= self.calculate_fee()

                signal -= 1

            #End long operation
            if (signal < 0 
                and self.operations
                and self.operations[-1].is_open
                and self.operations[-1].is_long()):

                #Update balance
                self.operations[-1].end(close, time)
                self.balance *= self.operations[-1].percentual_return

                #Count a win
                if self.operations[-1].percentual_return > 1:
                    self.win_rate+=1 

                #Update fees
                self.total_fees += self.calculate_fee()
                self.balance -= self.calculate_fee()

                signal += 1

            #Start short operation
            elif (signal < 0 
                  and not (self.operations 
                           and self.operations[-1].is_open)):

                #Start operation
                self.operations.append(Operation(close,time,'Short'))

                #Update fees
                self.total_fees += self.calculate_fee()
                self.balance -= self.calculate_fee()

                signal += 1

            self.ticker.data.loc[time,'Strategy Return'] = self.balance

        self.win_rate = 100*self.win_rate/len(self.operations)
        
        #Debug stuff
        '''for i in self.operations:
        
            print(f'Is open: {i.is_open}\n',
                  f'Start time: {i.start_time}\n',
                  f'End time: {i.end_time}\n',
                  f'Return: {i.percentual_return}\n')'''

        print(self.ticker.data[['Strategy Return','Buy and Hold','Close']])
        print(self.total_fees)
        print(len(self.operations))
        print(f'{self.win_rate:.2f}')


