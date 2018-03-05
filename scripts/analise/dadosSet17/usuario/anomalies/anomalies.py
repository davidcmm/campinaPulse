from __future__ import division
from itertools import izip, count
import matplotlib.pyplot as plt
from numpy import linspace, loadtxt, ones, convolve
import numpy as np
import pandas as pd
import collections
from random import randint
from matplotlib import style
style.use('fivethirtyeight')
import sys

# 3. Lets define some use-case specific UDF(User Defined Functions)

def moving_average(data, window_size):
	""" Computes moving average using discrete linear convolution of two one dimensional sequences.
	Args:
	-----
	    data (pandas.Series): independent variable
	    window_size (int): rolling window size

	Returns:
	--------
	    ndarray of linear convolution

	References:
	------------
	[1] Wikipedia, "Convolution", http://en.wikipedia.org/wiki/Convolution.
	[2] API Reference: https://docs.scipy.org/doc/numpy/reference/generated/numpy.convolve.html

	"""
	window = np.ones(int(window_size))/float(window_size)
	return np.convolve(data, window, 'same')


def explain_anomalies(y, window_size, sigma=1.0):
	""" Helps in exploring the anamolies using stationary standard deviation
	Args:
	-----
	y (pandas.Series): independent variable
	window_size (int): rolling window size
	sigma (int): value for standard deviation

	Returns:
	--------
	a dict (dict of 'standard_deviation': int, 'anomalies_dict': (index: value))
	containing information about the points indentified as anomalies

	"""
	avg = moving_average(y, window_size).tolist()
	residual = y - avg
	# Calculate the variation in the distribution of the residual
	std = np.std(residual)
	return {'standard_deviation': round(std, 3),
	    'anomalies_dict': collections.OrderedDict([(index, y_i) for
		                                       index, y_i, avg_i in izip(count(), y, avg)
	      if (y_i > avg_i + (sigma*std)) | (y_i < avg_i - (sigma*std))])}


def explain_anomalies_rolling_std(y, window_size, sigma=1.0):
	""" Helps in exploring the anamolies using rolling standard deviation
	Args:
	-----
	y (pandas.Series): independent variable
	window_size (int): rolling window size
	sigma (int): value for standard deviation

	Returns:
	--------
	a dict (dict of 'standard_deviation': int, 'anomalies_dict': (index: value))
	containing information about the points indentified as anomalies
	"""
	avg = moving_average(y, window_size)
	avg_list = avg.tolist()
	residual = y - avg
	# Calculate the variation in the distribution of the residual
	testing_std = pd.rolling_std(residual, window_size)
	testing_std_as_df = pd.DataFrame(testing_std)
	rolling_std = testing_std_as_df.replace(np.nan,
		                  testing_std_as_df.ix[window_size - 1]).round(3).iloc[:,0].tolist()
	std = np.std(residual)
	return {'stationary standard_deviation': round(std, 3),
	    'anomalies_dict': collections.OrderedDict([(index, y_i)
		                                       for index, y_i, avg_i, rs_i in izip(count(),
		                                                                           y, avg_list, rolling_std)
	      if (y_i > avg_i + (sigma * rs_i)) | (y_i < avg_i - (sigma * rs_i))])}


# This function is repsonsible for displaying how the function performs on the given dataset.
def plot_results(x, y, window_size, sigma_value=1,
                 text_xlabel="X Axis", text_ylabel="Y Axis", applying_rolling_std=False):
	""" Helps in generating the plot and flagging the anamolies.
	Supports both moving and stationary standard deviation. Use the 'applying_rolling_std' to switch
	between the two.
	Args:
	-----
	x (pandas.Series): dependent variable
	y (pandas.Series): independent variable
	window_size (int): rolling window size
	sigma_value (int): value for standard deviation
	text_xlabel (str): label for annotating the X Axis
	text_ylabel (str): label for annotatin the Y Axis
	applying_rolling_std (boolean): True/False for using rolling vs stationary standard deviation
	"""
	plt.figure(figsize=(15, 8))
	plt.plot(x, y, "k.")
	y_av = moving_average(y, window_size)
	plt.plot(x, y_av, color='green')
	plt.xlim(0, 1600)
	plt.xlabel(text_xlabel)
	plt.ylabel(text_ylabel)

	# Query for the anomalies and plot the same
	events = {}
	if applying_rolling_std:
        	events = explain_anomalies_rolling_std(y, window_size=window_size, sigma=sigma_value)
	else:
	        events = explain_anomalies(y, window_size=window_size, sigma=sigma_value)

	# Display the anomaly dict
	print("Information about the anomalies model:{}".format(events))

	x_anomaly = np.fromiter(events['anomalies_dict'].iterkeys(), dtype=int, count=len(events['anomalies_dict']))
	y_anomaly = np.fromiter(events['anomalies_dict'].itervalues(), dtype=float,
		                            count=len(events['anomalies_dict']))
	x_to_plot = [x[index] for index in x_anomaly]
	print( "Keys " + str( [ (x_to_plot[i], y_anomaly[i]) for i in range(0, len(x_to_plot)) ] ) )
	plt.plot(x_to_plot, y_anomaly, "r*", markersize=12)

	# add grid and lines and enable the plot
	plt.grid(True)
	plt.show()

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Uso: <arquivo de scores a avaliar>"
		sys.exit(1)

	data = pd.read_csv(sys.argv[1], sep="\t", header=0)

	# 2. View the data as a table
	data_as_frame = pd.DataFrame(data, columns=['num', 'qscore'])
	data_as_frame.head()

	# 4. Lets play with the functions
	x = data_as_frame['num']
	Y = data_as_frame['qscore']

	# plot the results
	plot_results(x, y=Y, window_size=2, text_xlabel="Street Num.", sigma_value=0.5,
		     text_ylabel="Scores")
	events = explain_anomalies(y, window_size=2, sigma=0.5)

	# Display the anomaly dict
	print("Information about the anomalies model:{}".format(events))
