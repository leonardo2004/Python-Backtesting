#Base:
import pandas as pd
import numpy as np
import datetime

#Custom:
import brain
import indicators
import plotting

def filter_signals_causal(signals, min_group_size=3):
    
    filtered_signals = signals.copy()
    n = len(signals)
    
    current_valid_value = 0
    last_invalid_value = 0
    new_group_size = 0
    invalidate_current_group = 0
    i = 0
    
    while i < n:
        if filtered_signals[i] != current_valid_value:
            invalidate_current_group += 1

            if last_invalid_value == filtered_signals[i]:
                new_group_size += 1
                

            else:
                last_invalid_value = filtered_signals[i]
                new_group_size = 1

            filtered_signals[i] = current_valid_value
            
        else:
            new_group_size = 0
            invalidate_current_group = 0

        if new_group_size >= min_group_size:
            current_valid_value = last_invalid_value
            last_invalid_value = None
        
        elif invalidate_current_group >= min_group_size:
            current_valid_value = 0
            filtered_signals[i] = current_valid_value

        i+=1
        
    return filtered_signals

INITIAL_BALANCE = 50
TRADING_FEE = 0 #Trading fee per OPERATION, in percentage (%)

#Time period
PERIOD_END = datetime.datetime.now()
PERIOD_DELTA = 59
PERIOD_START = PERIOD_END - datetime.timedelta(days=PERIOD_DELTA)

#Define ticker
ETH = brain.YFTicker('ETH-USD',PERIOD_START,PERIOD_END,'5m')

#Download and save ticker
#ETH.download()
#ETH.save_pkl('./Data/xrp5m.pkl')

#Load ticker from memory
ETH.load_pkl('./Data/eth5m.pkl')

#Define SMAs
ethsma5 = indicators.SMA(ETH, 7, 'Close')
#ethsma20 = indicators.SMA(ETH, 100, 'Close')

#Calculate signals based on the relative position of the smas
#signals = ethsma5.is_crossing(ethsma20)
signals = ethsma5.direction()
#signals = np.array([1, 1, 1, 0, -1, -1, -1, -1, 0, 1, 0, 0])
signals = filter_signals_causal(signals, min_group_size=14)


teste = brain.Strategy(signals, ETH, 500, trading_fee=0.05)
teste.run()
