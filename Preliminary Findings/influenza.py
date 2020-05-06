import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.dates as mdates

#fludatasw = pd.read_csv('usabledatasweden.csv')
fludataus = pd.read_csv('ususabledata.csv')
fludatasw = pd.read_csv('swedeninfluenzausable.csv')
fludatait = pd.read_csv('italyinfluenzausable.csv')

cases_by_week_sw = fludatasw['ALL_INF'].to_list()
dates_by_week_sw = fludatasw['EDATE'].to_list()

cases_by_week_it = fludatait['ALL_INF'].to_list()
dates_by_week_it = fludatait['EDATE'].to_list()

cases_by_week_us = fludataus['TOTAL PATIENTS'].to_list()
dates_by_week_us = dates_by_week_it[0:499]

logged_case_sw = np.log10(cases_by_week_sw)
logged_case_it = np.log10(cases_by_week_it)
logged_case_us = np.log10(cases_by_week_us)

plt.figure(figsize = (15,7))
plt.xticks(rotation = 90)
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(12))

plt.plot(dates_by_week_sw, logged_case_sw, label = 'Sweden')
plt.plot(dates_by_week_it, logged_case_it, label = 'Italy')
plt.plot(dates_by_week_us, logged_case_us, label = 'United States')
#plt.plot(dates_by_week_sw, cases_by_week_sw, label = 'Sweden')
#plt.plot(dates_by_week_it, cases_by_week_it, label = 'Italy')
#plt.plot(dates_by_week_us, cases_by_week_us, label = 'United States')
plt.title('Influenza Cases Over Time (logged)')
plt.legend()
plt.show()

xsw = range(len(dates_by_week_sw))
xit = range(len(dates_by_week_it))
xus = range(len(dates_by_week_us))

data = {
    'x': xsw,
    'y': logged_case_sw
}

data['y_p'] = np.diff(data['y']) / np.diff(data['x'])
data['x_p'] = (np.array(data['x'])[:-1] + np.array(data['x'])[1:]) / 2


data2 = {
    'x2': xit,
    'y2': logged_case_it
}

data2['y2_p'] = np.diff(data2['y2']) / np.diff(data2['x2'])
data2['x2_p'] = (np.array(data2['x2'])[:-1] + np.array(data2['x2'])[1:]) / 2

data3 = {
    'x': xus,
    'y': logged_case_us
}

data3['y_p'] = np.diff(data3['y']) / np.diff(data3['x'])
data3['x_p'] = (np.array(data3['x'])[:-1] + np.array(data3['x'])[1:]) / 2

logged_diff_sw = np.log10(data['y_p'])
logged_diff_it = np.log10(data2['y2_p'])
logged_diff_us = np.log10(data3['y_p'])

#plt.plot(dates_by_week_sw[1:], data['y_p'], label = 'Sweden')
#plt.plot(dates_by_week_it[1:], data2['y2_p'], label = 'Italy')
#plt.plot(dates_by_week_us[1:], data3['y_p'], label = 'United States')
#plt.title('Influenza Case Rate Over Time (logged)')
#plt.legend()
#plt.show()