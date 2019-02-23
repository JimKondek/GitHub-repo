# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 12:03:06 2019

@author: Jim
"""

import random
from timeit import default_timer as timer

list_length = 10000
z = random.sample(range(list_length * 2), list_length)
x = z.copy()
y = z.copy()

start = timer()

for j in range(0, list_length - 1):
    for i in range(0, list_length - 1):
        if x[i] > x[i + 1]:
            hold = x[i + 1]
            x[i + 1] = x[i]
            x[i] = hold

end = timer()
print('1st sort elapsed time:  {}'.format(end - start))

start = timer()

incr = list_length
while incr > 0:
    for i in range(0, incr - 1):
        if y[i] > y[i + 1]:
            hold = y[i + 1]
            y[i + 1] = y[i]
            y[i] = hold
    incr = incr - 1

end = timer()
print('2nd sort elapsed time:  {}'.format(end - start))

if x == y:
    print('Results are the same.')
else:
    print('Results are different.')

# print(z)
# print(y)
# print(x)
