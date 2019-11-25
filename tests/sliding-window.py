import unittest

import numpy as np
import matplotlib.pyplot as plt

from changepoint.algorithms.OnlineChangePoint import OnlineChangePoint



'''
Test window-based change point detection for streaming data
'''
class SlidingWindowTestCase(unittest.TestCase):

    def test_changepoint_detection(self):

        # Create a synthetic data set to test with
        np.random.seed(42)  # Reproducible test cases
        points = np.concatenate([np.random.normal(loc=500, scale=5, size=550),
                                 np.random.normal(loc=750, scale=5, size=25),
                                 np.random.normal(loc=500, scale=5, size=250)]).tolist()

        # Diagram the data set
        plt.plot(points)
        plt.show()

        classifier: OnlineChangePoint = OnlineChangePoint()

        for counter, value in enumerate(points):
            category = classifier.classify(value)
            print( f'{counter} => {value}, {category}')

        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
