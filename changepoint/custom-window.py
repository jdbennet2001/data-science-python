import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from statistics import mean, stdev
from math import fabs

from changepoint.algorithms.OnlineChangePoint import  OnlineVariance

# Define a Window size for analysis.
# Anomalies only count if they register for 'n' points in a row
WINDOW_SIZE:int = 5

# Create a synthetic data set to test with
points = np.concatenate([np.random.normal(loc=500, scale=5, size=550),
                         np.random.normal(loc=750, scale=5, size=15),
                         np.random.normal(loc=500, scale=5, size=250)]).tolist()


# Walk all data points
length: str = len(points)

# Standard deviation counters
s0 = 0
s1 = 0
s2 = 0

# Seed running totals to prevent divide by zero error
for i in range( 0, WINDOW_SIZE):
    x = points[i]

    # Keep running totals for std deviation calculations
    s0 = s0 + 1             # Total number of samples
    s1 = s1 + x             # Running total
    s2 = s2 + (x * x)       # Running total squares


for i in range(WINDOW_SIZE, len(points) - WINDOW_SIZE ):

    # Generate the new window
    x  = points[i]
    pre:list  = points[i-WINDOW_SIZE: i]
    post:list = points[i: i + WINDOW_SIZE]
    # print( f'{i} => {pre}, {post}')

    # metadata...
    delta = fabs( mean(pre)  - mean(post) )
    size  = fabs( stdev(pre) - stdev(post) )

    anomoly = (delta > fabs( 3 * stdev(pre)) )


    # Keep running totals for std deviation calculations
    print( f'{i} => {anomoly}')

