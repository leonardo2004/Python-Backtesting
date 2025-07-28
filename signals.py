import pandas as pd
import numpy as np

def SMA_direction(column: str, series: pd.Series, delta = 0):
    """
        THIS FUNCTIONS CHECKS IF THE SMA IS GOING UP OR DOWN BASED ON THE PREVIOUS VALUE
        IT RETURNS A SIGNAL NUMPY LIST: 1 == TRUE, 0 == NONE, -1 == FALSE

        PARAMNS:
            series: pd.Series -> INPUT THE SMA SERIES
            delta: float -> DELTA, MINIMUM VARIATION REQUIRED
    """
    #.shift(1) -> GETS THE VALUE OF THE PREVIOUS LINE
    signal = np.where((series>((1 + delta) * series.shift(1))),1,0)
    signal = np.where((series<((1 - delta) * series.shift(1))),-1,signal)
    return signal

def SMA_loc(columnA: str, columnB: str, ticker: pd.DataFrame, delta = 0):
    """
        THIS FUNCTIONS CHECKS WHERE THE SMA IS COMPARED TO ANOTHER
        IT RETURNS A SIGNAL NUMPY LIST: 1 == ABOVE, 0 == NONE, -1 == BELOW

        PARAMNS:
            columnA: str -> THE SMA COLUMN ABOVE
            columnB: str -> THE SMA COLUMN BELOW
            ticker: pd.DataFrame -> ticker DATAFRAME
            delta: float -> DELTA, MINIMUM VARIATION REQUIRED
    """
    #.shift(1) -> GETS THE VALUE OF THE PREVIOUS LINE
    signal = np.where((ticker[columnA]>((1 + delta) * ticker[columnB].shift(1))),1,0)
    signal = np.where((ticker[columnA]<((1 - delta) * ticker[columnB].shift(1))),-1,signal)
    return signal
