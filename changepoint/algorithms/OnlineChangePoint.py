import numpy as np

from statistics import mean, stdev
from math       import fabs, sqrt

'''
Changepoint detection for a stream of named data
'''
class OnlineChangePoint:

    def __init__(self, name='unknown', deviation=3, window_size=5):
        self.VARIANCE = deviation
        self.WINDOW_SIZE = window_size
        self.NAME = name

        # Running totals
        self.s0 = 0 # Total number of samples
        self.s1 = 0 # Running total
        self.s2 = 0 # Running total squares

        self.BUFFER_SIZE = 2 * window_size
        self.buffer:list = []

    '''
    Classify a data point as a changepoint
    @param  {number} - Point to be classified
    @return {bool}   - Point represents a new window shift
    '''
    def classify(self, value):
        self.buffer.append(value)

        # Stream metadata..
        self.s0 += 1
        self.s1 += value
        self.s2 += value * value

        if len(self.buffer) < self.BUFFER_SIZE:
            return

        #Drop extra item(s) from list
        if len(self.buffer) > self.BUFFER_SIZE:
            self.buffer = self.buffer[-self.BUFFER_SIZE:]

        variance:float = self.__variance()

        return self.__isChangePoint(self.buffer, variance)



    '''
    How noisy is the data?
    '''
    def __variance(self):
        s0 = self.s0
        s1 = self.s1
        s2 = self.s2

        std_dev = sqrt((s0 * s2 - s1 * s1) / (s0 * (s0 - 1)))

        return self.VARIANCE * std_dev


    def __isChangePoint(self,points, noise):

        # Break the data into two groups and validate
        w1: list = points[:self.WINDOW_SIZE]
        w2: list = points[-self.WINDOW_SIZE:]

        # How big a change is this?
        delta:float = fabs(mean(w1) - mean(w2))

        return delta > noise
