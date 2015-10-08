#!/usr/bin/env python
__author__ = 'will'
import numpy as np
import pandas as pd

from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy import *
from scipy.optimize import leastsq

f = open("Predict2014b.csv", "r")
header = f.readline()


milkProductionByMonth = []

for row in f:
    components = row.split("\t")
    if components[3] is "":
        if len(components) <= 3:  # we are dealing with missing data
            milkProductionByMonth.append(np.nan)
        else:  # we are dealing with the data being shifted over by a column
            productionInCurrentMonth = 0
            try:
                productionInCurrentMonth = float(components[4])
            except ValueError:
                milkProductionByMonth.append(np.nan)
            else:
                milkProductionByMonth.append(productionInCurrentMonth)
    else:
        milkProductionByMonth.append(float(components[3]))
milkProductionByMonth = np.array(milkProductionByMonth)
'''
now we have read the data about the milk production into an array that is n numpy array.
This arrays hold data of milk production by month in units of millions of pounds.
'''
x = np.array(range(len(milkProductionByMonth)))  # creates an x-axis to use for graphing

x_date_range = pd.date_range('1930-01-01', periods=1020, freq="M")  # was 1006

#'''
#plt.plot(x, milkProductionByMonth, c="Red", linewidth=1)
#plt.scatter(x, milkProductionByMonth, c="Blue")
#plt.xlim(min(x), max(x))
plt.plot(x_date_range, milkProductionByMonth, c="Red", linewidth=1)
plt.scatter(x_date_range, milkProductionByMonth, c="Blue")
plt.xlabel("Time By Month", fontsize=30)
plt.ylabel("Milk Production - Millions of Pounds", fontsize=30)
plt.show()
#'''

'''
sinusoidal modeling modeling
'''
'''
month_count = 360
shortx = x[:month_count] # do 30 years: 360 months
shorty = milkProductionByMonth[:month_count]
sinx = np.sin(2*np.pi*shortx/12.0)
cosx = np.cos(2*np.pi*shortx/12.0)
#optFunc = lambda p: p[0] + p[1]*sinx + p[2]*cosx - shorty
optFunc = lambda p: p[0] + p[1]*sinx + p[2]*cosx + p[3]*shortx - shorty
coeffs = leastsq(optFunc, [1, 1, 1, 1])[0]

xWithManyPoints = np.linspace(0, max(shortx), 500)
newsinx = np.sin(2*np.pi*xWithManyPoints/12.0)
newcosx = np.cos(2*np.pi*xWithManyPoints/12.0)
y_fit = coeffs[0] + coeffs[1]*newsinx + coeffs[2]*newcosx + coeffs[3]*xWithManyPoints


'''

#plotting of the first 360 months
'''
short_x_date_range = pd.date_range('1930-01-01', periods=len(shortx), freq="M")

plt.plot(shortx, shorty, c="red", linewidth=1)
plt.scatter(shortx, shorty)

#sinusoidalFunction = str(coeffs[0]) + " + " + str(coeffs[1]) + " * sin(2*pi*x/12) + " + \
#                     str(coeffs[2]) + " * cos(2*pi*x/12) + " + str(coeffs[3]) + " * x" % (coeffs[0], coeffs[1], str(coeffs[2], coeffs[3])
sinusoidalFunction = "%.2f + %.2f * sin(2*pi*x/12) + %.2f * cos(2*pi*x/12) + %.2f * x" % (coeffs[0], coeffs[1], coeffs[2], coeffs[3])
plt.plot(xWithManyPoints, y_fit, label=sinusoidalFunction, c="green")
plt.xlim(min(shortx), max(shortx))
plt.xlabel("Month", fontsize=30)
plt.ylabel("Milk Production - Millions of Pounds", fontsize=30)
plt.legend(loc="upper left", fontsize=15)
plt.show()
'''
#f.close()