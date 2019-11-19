import numpy as np
import pandas as pd

data_baseline = np.random.normal(loc=500, scale=5, size=550)
print(data_baseline.shape)
data_breakout = np.random.normal(loc=750, scale=5, size=100)
print(data_breakout.shape)
type(data_baseline)

data_all = np.concatenate((data_baseline, data_breakout))

ts = pd.Series(data_all)
ts.plot.line()

print( 'Done')