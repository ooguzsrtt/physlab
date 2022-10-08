import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sb
from sympy import S, symbols, printing

sb.set()
matplotlib.use('TkAgg')

situation = 'real'  # real / sim

if situation == 'real':
    csv_file = 'constant-motion.csv'  # csv file name
    csv_data = pd.read_csv(csv_file, sep=';', usecols=[0, 1])  # read csv file
    csv_data = csv_data.dropna()  # drop NaN values
    time_data = csv_data['Time']  # define time_data
    location_data = csv_data['Location']  # define location_data
else:
    frequency = 1 / 10  # frequency of spark
    timer = 1  # total time of motion in seconds
    deviation = .1  # deviation from perfection  by integer value in a range
    #                 for example deviation=10 means range of [value-5, value+5]
    error_rate = 1  # amount of data will be manipulated in data set by percentage
    expected_velocity = 1  # expected velocity in cm/s
    time_data = np.arange(start=frequency, stop=timer + frequency, step=frequency)
    # spark simulation in "timer" seconds, respect to frequency = 1/period
    location_data = np.multiply(expected_velocity, time_data)
    # perfect location data with respect to expected_velocity
    # using the formula x=vt
    location_data = location_data.astype(float)
    # set location_data array as float data array
    choice_array = np.random.choice(location_data.size, round(location_data.size * error_rate), replace=False)
    # make random location choices with respect to error_rate variable defined above
    location_data.flat[choice_array] += np.random.uniform(low=-float(deviation / 2),
                                                          high=float(deviation / 2),
                                                          size=round(location_data.size * error_rate))
    # deviate the chosen locations from perfection with respect to the variable "deviation".

data_dict = {
    "location": location_data,
    "time": time_data
}
# define a dict for pandas DataFrame

data = pd.DataFrame(data_dict)  # create a pandas DataFrame
reg = np.polyfit(data['time'], data['location'], deg=1)  # define linear regression polynomial
trend = np.polyval(reg, data['time'])  # passing the time values on linear regression polynomial
plt.scatter(x=data['time'], y=data['location'])  # scatter simulated/real life graph

# create latex equation for display the linear regression polynomial
t = symbols("t")
poly = sum(S("{:6.2f}".format(v)) * t ** i for i, v in enumerate(reg[::-1]))
eq_latex = printing.latex(poly)

# plot all the data
plt.plot(data['time'], trend, 'r', label="${}$".format(eq_latex))

plt.legend(fontsize="small")  # font size

print("Slope of the linear regression line is: {}".format(reg[0]))
# print slope

plt.show()  # show plot
