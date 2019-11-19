import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ruptures as rpt


# Create a synthetic data set to test with
points = np.concatenate([np.random.normal(loc=500, scale=5, size=550),
                         np.random.normal(loc=750, scale=5, size=25),
                         np.random.normal(loc=500, scale=5, size=250)])

algo = rpt.Pelt(model="rbf", jump=5).fit(points)
result = algo.predict(pen=10)

plt.plot(points)
plt.show()

print( f'Pelt analysis: {result}' )