import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt

class YFTicker():
    def __init__(self, name: str, start: dt.datetime, end: dt.datetime, time_interval: str):
        self.name = name
        self.start = start
        self.end = end
        self.time_interval = time_interval

    #downloads the ticker from yfinance
    def Download(self, fill_method = '', drop_na=False, drop_zero=False):
        self.data = yf.download(
            self.name,
            start=self.start,
            end=self.end,
            interval=self.time_interval,
            auto_adjust=True,
        multi_level_index=False
        ).loc[:,["Open","High","Low","Close","Volume"]].round(2)
    
        #fill nan values using the selected method
        if fill_method == 'ffill':
            self.data.ffill(inplace=True)
        elif fill_method == 'bfill':
            self.data.bfill(inplace=True)
        elif fill_method == 'interpolate':
            self.data.interpolate(inplace=True)
        
        #drop zeros
        if drop_zero:
            self.data.replace(to_replace=0,value=np.nan,inplace=True)

        #drop na
        if drop_na:
            self.data.dropna(inplace=True)

    #saves ticker as .pkl file
    def SavePKL(self, path="./ticker.pkl"):
        self.data.to_pickle(path)

    #loads ticker as .pkl file
    def LoadPKL(self, path="./ticker.pkl"):
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

def run_strategy(ticker: pd.DataFrame, fee: float, initial_balance: float):
    val = line = total_operations = win_operations = total_fee = profit = 0

    balance = initial_balance
    ticker["Strategy_Return"] = pd.Series(0)

    #Run strategy:
    for i in ticker.Entry:
        if (i > 0):
            if (val == -1 or i == 2):
                #SELL END
                delta = start - ticker["Close"].iat[line]
                if delta > 0:
                    win_operations += 1
                print(f"SHORT {balance:.2f} {(delta*balance)/start:.2f} {ticker["Entry"].iat[line]} LINE {line}")

                profit = (delta*balance)/start
                balance += profit
                ticker["Strategy_Return"].iat[line] = profit

                val = 0
            if (val == 0):
                #BUY START
                total_fee += balance * (fee / 100)
                total_operations += 1
                start = ticker["Close"].iat[line]
                val = 1

        elif (i < 0):
            if (val == 1 or i == -2):
                #BUY END
                delta = ticker["Close"].iat[line] - start
                if delta > 0:
                    win_operations += 1
                print(f"LONG {balance:.2f} {(delta*balance)/start:.2f} {ticker["Entry"].iat[line]} LINE {line}")

                profit = (delta*balance)/start
                balance += profit
                ticker["Strategy_Return"].iat[line] = profit

                total_fee += balance * (fee / 100)
                val = 0
            if (val == 0):
                #SELL START
                total_fee += balance * (fee /100)
                total_operations += 1
                start = ticker["Close"].iat[line]
                val = -1

        line += 1


    #Strategy return calculation:
    ticker["Strategy_Return"] = ticker["Strategy_Return"].fillna(0)

    #Buy and Hold return:
    bnh_total_return = ticker["Close"].iat[-1] - ticker["Close"].iat[0]
    bnh_percentual_return = (bnh_total_return*100)/(ticker["Close"].iat[0])

    #Printing results:    
    print("\n\n"+"~"*16+"Results:"+"~"*16)
    print(f"Total operations: {total_operations}")
    print(f"Win operations: {win_operations}")
    if total_operations > 0:
        print(f"Win percentage: {win_operations / total_operations *100:.2f}%")
    else:
        print("Win percentage: 0.00%")
    print(f"Total fees: {total_fee:.2f}")
    print(f"Buy Hold return: {bnh_percentual_return:.2f}%")
    print(f"Strategy return: {((balance-initial_balance)*100/initial_balance):.2f}%")
    print(f"Balance: {((balance)-total_fee):.2f}")
    print(f"Profit: {((balance - initial_balance)-total_fee):.2f}")
    return
