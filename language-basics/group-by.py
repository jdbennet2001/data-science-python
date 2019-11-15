import itertools

import numpy as np
import pandas as pd

'''
Group a stream of data by a single field
'''



data_set: list = []

# Generate a hundred tuples of the form {value: number, id: string}
for num in range(100):
    id:str = 'A' if num % 3 == 0 else 'B'
    value:dict = {"value": num, "id": id}
    data_set.append(value)

# itertools groupby support requires the data to be sorted..
sorted_data = sorted(data_set, key = lambda x: x['id'])

# Now we can group everything, which give an iterable back
for key, group in itertools.groupby(sorted_data, lambda x: x['id']):
    items = list(group)
    print( key, items )

# We can cast to a dict, but you get Map(<string>key, <iterable>values)
groped_data = dict(itertools.groupby(sorted_data, lambda x: x['id']))

# print(*data_set)