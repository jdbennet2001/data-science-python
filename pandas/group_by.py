import itertools

import numpy as np
import pandas as pd

from datetime   import datetime, timedelta

'''
Implement sample data + 'group by' support to test breakout detection 
'''

'''
Round a floating point number to 'n' significant figures
'''
def round_to_n(x, n):
    fmt = '{:1.' + str(n) + 'e}'    # gives 1.n figures
    p = fmt.format(x).split('e')    # get mantissa and exponent
                                    # round "extra" figure off mantissa
    p[0] = str(round(float(p[0]) * 10**(n-1)) / 10**(n-1))
    return float(p[0] + 'e' + p[1]) # convert str to float

'''
 Generate a series of data points, one per minute
 
 @typdef   {object} seed
 @property {string} service
 @property {number} requests (count number of incoming (server) datapoints)
 @property {number} reliability ( (requests-errors) / requests)
 @property {number} duration (cpu/requests)
 
 @param     {seed}   seed        - basic service level
 @param     {number} [start]     - integer minutes from start of data generation
 @param     {number} [end]       - integer minutes from start of data generation
 @param     {number} [variance]  - perecent deviation of results 
 @return    {[seed]} 
'''
def data(seed, start, end, variance):

    # Let's pick an arbitrary starting point
    start_time:datetime = datetime(year=2017, month=11, day=28, hour=23, minute=55)

    request_level = seed['requests']
    request_scale = request_level * variance

    reliability_level = seed['reliability']
    error_level = int(request_level * ( 1 - reliability_level))
    error_scale = error_level * variance

    duration_level = seed['duration']
    duration_scale = duration_level * variance

    datapoints:list = []

    for delta in range(start, end):

        # timestamp
        timestamp = start_time + timedelta(0, 0, 0, 0, delta)
        timestamp = timestamp.strftime("%Y %m %d : %H:%M:%S")

        # request data
        requests = int(np.random.normal(loc=request_level, scale=request_scale))
        errors   = int(np.random.normal(loc=error_level, scale=error_scale))

        # statistics
        reliability = (requests - errors) / requests
        reliability = round_to_n(reliability, 3)

        # duration
        duration = int(np.random.normal(loc=duration_level, scale=duration_scale))

        # result
        datapoint = {"requests" : requests, "errors" : errors,
                     "reliability" : reliability, "duration" : duration,
                     "timestamp" : timestamp, "service" : seed['service']}

        datapoints.append(datapoint)

    return datapoints

seed:dict = {"service": "data", "requests" : 500, "reliability": 0.99, "duration": 650}

datapoints = data(seed, start=0, end=360, variance=0.1)
print(datapoints)

