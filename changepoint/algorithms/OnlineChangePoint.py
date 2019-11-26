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

        # We need 'window_size' outliers in a row to trigger a change
        self.outliers:list = [False] * window_size

        # Running totals
        self.s0 = 0 # Total number of samples
        self.s1 = 0 # Running total
        self.s2 = 0 # Running total squares

        # Debug ctr
        self.ctr = 0

        self.BUFFER_SIZE = 2 * window_size
        self.buffer:list = []

    '''
    Classify a data point as a changepoint
    @param  {number} - Point to be classified
    @return {bool}   - Point represents a new window shift
    '''
    def classify(self, value):

        self.buffer.append(value)

        self.ctr += 1

        if len(self.buffer) < self.BUFFER_SIZE:
            self._updateRunningStats(value)
            return

        #Drop extra item(s) from list
        if len(self.buffer) > self.BUFFER_SIZE:
            self.buffer = self.buffer[-self.BUFFER_SIZE:]

        variance: float = self._variance()
        threshold: float = self.VARIANCE * variance

        outlier, delta =  self.__isChangePoint(self.buffer, threshold)

        if ( not outlier ):
            self._updateRunningStats(value)

        self.outliers.append(outlier)
        self.outliers = self.outliers[-self.WINDOW_SIZE:]

        changepoint = all(self.outliers)

        if changepoint:
            self._resetRunningStats()

        return changepoint


    '''
    How noisy is the data?
    '''
    def _updateRunningStats(self, value):
        # Stream metadata..
        self.s0 += 1
        self.s1 += value
        self.s2 += value * value


    def _variance(self):

        s0 = self.s0
        s1 = self.s1
        s2 = self.s2

        std_dev = 0 \
            if (s0 == 1 or s0 == 0) \
            else sqrt((s0 * s2 - s1 * s1) / (s0 * (s0 - 1)))

        return std_dev


    '''
    New group, update the running counters
    '''
    def _resetRunningStats(self):
        # self.s0 = 0
        # self.s1 = 0
        # self.s2 = 0

        self.outliers = [False] * self.WINDOW_SIZE
        self.buffer = []


    def __isChangePoint(self,points, noise):

        # Break the data into two groups and validate
        w1: list = points[:self.WINDOW_SIZE]
        w2: list = points[-self.WINDOW_SIZE:]

        # How big a change is this?
        delta:float = fabs(mean(w1) - mean(w2))

        changepoint = delta > noise

        return changepoint, delta
