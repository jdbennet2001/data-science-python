import itertools

import numpy as np
import pandas as pd

'''
Walk through Natasha's use of Pandas to group data by a single field
'''

'''
Seperate data into two groups, 'A' and 'B'
'''
def get_id(count):
    if count % 3 == 0:
        return  "A"
    else:
         return  "B"

data_set: list = []

# Generate a hundred tuples of the form {value: number, id: string}
for num in range(100):
    value:dict = {"value": num, "id": "id_" + get_id(num)}
    data_set.append(value).av

df = pd.DataFrame(data_set)
print(df)

# group the data by id
group = df.groupby("id")

group

print(group)

# print(*data_set)