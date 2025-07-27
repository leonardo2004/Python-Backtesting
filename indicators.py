import pandas as pd
import numpy as np
import brain as br

def VWAP(ticker: pd.DataFrame):
    """
    WIP
        THIS FUNCTION GENERATES THE VWAP, CREATING PANDAS 
    """
    try:
        vwap = np.array((((ticker["High"] + ticker["Low"] + ticker["Close"]) * 
                       (ticker["Volume"]).cumsum()) / 
                      (3 * ticker["Volume"].cumsum())))
    except:
        print("Error: Could not generate VWAP")
    return vwap

class SMA():
    def __init__(self,ticker: br.YFTicker, sma_window: int, column: str):
        """
            CREATES A SIMPLE MOVING AVERAGE BASED ON A COLUMN
            PARAMNS:
                ticker: YFTicker -> Ticker.data
                SMA_window: INT -> WINDOW OF THE SMA, EX: 20
                column: str -> Selects which column from data is going to create the sma

        """
        #Create the SMA
        self.values = (ticker.data[column].rolling(window=sma_window).mean().shift()).fillna(0)

    def direction(self, filter_type: str, delta = 0):
        dir = np.where((self.values>((1 + delta) * self.values.shift(1))),1,0)
        dir = np.where((self.values<((1 - delta) * self.values.shift(1))),-1, dir)
        return dir