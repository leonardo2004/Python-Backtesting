#Base:
import pandas as pd
import numpy as np
import datetime

#Custom:
import brain
import indicators
import signals
import plotting

"""
TO-DO:
    Code:
    * Code optimization
    * Code documentation
        * Roadmap (Skill tree like)

    Functionality:
        * Parameter optimization

    Strategies:
        * Volume strategy

Rules:
    snake_case for variables, functions and methods
    PascalCase for classes
    SCREAMING_SNAKE_CASE for constants
"""


INITIAL_BALANCE = 50
TRADING_FEE = 0 #Trading fee per OPERATION, in percentage (%)

#Time period
PERIOD_END = datetime.datetime.now()
PERIOD_START = PERIOD_END - datetime.timedelta(days=8)


ETH = brain.YFTicker('ETH-USD',PERIOD_START,PERIOD_END,'5m')
#ETH.Download()
#ETH.SavePKL('./Data/ticker.pkl')
ETH.LoadPKL('./Data/eth5m.pkl')
print(ETH.data.round(2))
print(ETH.data)


#Create SMAs
#Close
'''BTC = indicators.SMA(ticker=BTC, 
                    SMA_window=5, 
                    column="Close")
BTC = indicators.SMA(ticker=BTC, 
                    SMA_window=20, 
                    column="Close")
BTC = indicators.SMA(ticker=BTC, 
                    SMA_window=200,
                    column="Close")'''



#Calculate the signals for the 3 MA strategy
#If the 3 are pointing up == BUY
#If the 3 are pointing down == SELL
'''BTC["Signals"] = np.where((signals.SMA_direction("5_Close_SMA", BTC)==1) &
                          (signals.SMA_direction("20_Close_SMA", BTC)==1) &
                          (signals.SMA_direction("200_Close_SMA", BTC)==1),
                          1,
                          0)
BTC["Signals"] = np.where((signals.SMA_direction("5_Close_SMA", BTC)==-1) &
                          (signals.SMA_direction("20_Close_SMA", BTC)==-1) &
                          (signals.SMA_direction("200_Close_SMA", BTC)==-1),
                          -1,
                          BTC["Signals"])
'''

#Entry calculation 
# BUY position if Signal == 1; else end order
# SELL position if Signal == -1; else end order
'''BTC["Entry"] = BTC.Signals.diff()'''



#brain.run_strategy(ticker=BTC, fee=TRADING_FEE, initial_balance=INITIAL_BALANCE)
#plotting.plot_results(BTC)