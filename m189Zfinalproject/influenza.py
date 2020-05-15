import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.tsa.stattools import acf, pacf
import datetime as dt
import matplotlib.dates as mdates


plt.figure(figsize = (15,7))

#fludatasw = pd.read_csv('usabledatasweden.csv')
fludataus = pd.read_csv('ususabledata2.csv')
fludatasw = pd.read_csv('swedeninfluenzausable2.csv')
fludatait = pd.read_csv('italyinfluenzausable2.csv')

cases_by_week_sw = fludatasw['ALL_INF']
dates_by_week_sw = pd.to_datetime(fludatasw['EDATE'].astype(str), format = '%m/%d/%Y')

cases_by_week_it = fludatait['ALL_INF']
dates_by_week_it = pd.to_datetime(fludatait['EDATE'].astype(str), format = '%m/%d/%Y')

cases_by_week_us = fludataus['TOTAL PATIENTS']
dates_by_week_us = dates_by_week_it[0:500]

#logged_case_sw = np.log10(cases_by_week_sw)
#logged_case_it = np.log10(cases_by_week_it)
#logged_case_us = np.log10(cases_by_week_us)

#plt.figure(figsize = (15,7))
#plt.xticks(rotation = 90)
#plt.gca().xaxis.set_major_locator(plt.MultipleLocator(12))

#plt.plot(dates_by_week_sw, logged_case_sw, label = 'Sweden')
#plt.plot(dates_by_week_it, logged_case_it, label = 'Italy')
#plt.plot(dates_by_week_us, logged_case_us, label = 'United States')

#plt.plot(dates_by_week_sw, cases_by_week_sw, label = 'Sweden')
#plt.plot(dates_by_week_it, cases_by_week_it, label = 'Italy')
#plt.plot(dates_by_week_us, cases_by_week_us, label = 'United States')

us2019 = dates_by_week_us  > '2018-09-30'
usweek40date = dates_by_week_us[us2019]
usweek40case = cases_by_week_us[us2019]

#plt.plot(usweek40date, usweek40case, label = 'United States')

#plt.title('Influenza Cases Over Time')
#plt.legend()
#plt.show()

xsw = range(len(dates_by_week_sw))
xit = range(len(dates_by_week_it))
xus = range(len(dates_by_week_us))

data = {
    'x': xsw,
    'y': cases_by_week_sw
}

data['y_p'] = np.diff(data['y']) / np.diff(data['x'])
data['x_p'] = (np.array(data['x'])[:-1] + np.array(data['x'])[1:]) / 2


data2 = {
    'x2': xit,
    'y2': cases_by_week_it
}

data2['y2_p'] = np.diff(data2['y2']) / np.diff(data2['x2'])
data2['x2_p'] = (np.array(data2['x2'])[:-1] + np.array(data2['x2'])[1:]) / 2

data3 = {
    'x': xus,
    'y': cases_by_week_us
}

data3['y_p'] = np.diff(data3['y']) / np.diff(data3['x'])
data3['x_p'] = (np.array(data3['x'])[:-1] + np.array(data3['x'])[1:]) / 2

xus2 = range(len(usweek40date))

data4 = {
    'x': xus2,
    'y': usweek40case
}

data4['y_p'] = np.diff(data4['y']) / np.diff(data4['x'])
data4['x_p'] = (np.array(data4['x'])[:-1] + np.array(data4['x'])[1:]) / 2



sw2019 = dates_by_week_sw  > '2018-09-30'

swweek40date = dates_by_week_sw[sw2019]
swweek40case = cases_by_week_sw[sw2019]
xsw2 = range(len(swweek40date))
data5 = {
    'x': xsw2,
    'y': swweek40case
}
data5['y_p'] = np.diff(data5['y']) / np.diff(data5['x'])
data5['x_p'] = (np.array(data5['x'])[:-1] + np.array(data5['x'])[1:]) / 2

it2019 = dates_by_week_it  > '2018-09-30'
itweek40date = dates_by_week_it[it2019]
itweek40case = cases_by_week_it[it2019]
xit2 = range(len(itweek40date))
data6 = {
    'x': xit2,
    'y': itweek40case
}
data6['y_p'] = np.diff(data6['y']) / np.diff(data6['x'])
data6['x_p'] = (np.array(data6['x'])[:-1] + np.array(data6['x'])[1:]) / 2

#logged_diff_sw = np.log10(data['y_p'])
#logged_diff_it = np.log10(data2['y2_p'])
#logged_diff_us = np.log10(data3['y_p'])

#plt.plot(dates_by_week_sw[1:], data['y_p'], label = 'Sweden')
#plt.plot(dates_by_week_it[1:], data2['y2_p'], label = 'Italy')
plt.plot(dates_by_week_us[1:], data3['y_p'], label = 'United States')


#plt.plot(usweek40date[1:], data4['y_p'], label = 'United States')

#plt.plot(swweek40date[1:], data5['y_p'], label = 'Sweden')

#plt.plot(itweek40date[1:], data6['y_p'], label = 'Italy')

#plt.axvline(dt.datetime(2020, 3, 9), color = 'red')

plt.fill_between([dt.datetime(2020, 3, 19), dt.datetime(2020, 4, 7)], 350000, -350000, color='blue', alpha=0.1)


plt.xticks(rotation = 45)
plt.xlabel('Date')
plt.ylabel('Case Rate')
plt.title('Influenza Case Rate Over Time')
plt.legend()
plt.show()




