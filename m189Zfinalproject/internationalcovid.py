import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.dates as mdates
import datetime as dt

raw_confirmed = pd.read_csv('global.csv')
confirmed = raw_confirmed.drop(['Lat','Long'], axis = 1)

def set_country_res(df):

    df_sans_provinces = df.drop('Province/State', axis=1)
    df_sans_provinces = df_sans_provinces.groupby('Country/Region').sum()
    
    return df_sans_provinces

confirmed = set_country_res(confirmed)



confirmed.head()
confirmed.columns = pd.to_datetime(confirmed.columns)

plt.figure(figsize = (10,7))
plt.xticks(rotation = 45)
#plt.plot(confirmed.columns, confirmed.loc['US'], label = 'US')
#plt.plot(confirmed.columns, confirmed.loc['Sweden'], label = 'Sweden')
#plt.plot(confirmed.columns, confirmed.loc['Italy'], label = 'Italy')

dates = confirmed.columns.to_list()

confirmed_us = confirmed.loc['US']
confirmed_us = confirmed_us.to_list()
xus = range(len(confirmed_us))
data = {
    'x': xus,
    'y': confirmed_us
}
data['y_p'] = np.diff(data['y']) / np.diff(data['x'])
data['x_p'] = (np.array(data['x'])[:-1] + np.array(data['x'])[1:]) / 2

confirmed_sw = confirmed.loc['Sweden']
confirmed_sw = confirmed_sw.to_list()
xsw = range(len(confirmed_sw))
data1 = {
    'x': xsw,
    'y': confirmed_sw
}
data1['y_p'] = np.diff(data1['y']) / np.diff(data1['x'])
data1['x_p'] = (np.array(data1['x'])[:-1] + np.array(data1['x'])[1:]) / 2

confirmed_it = confirmed.loc['Italy']
confirmed_it = confirmed_it.to_list()
xit = range(len(confirmed_it))
data2 = {
    'x': xit,
    'y': confirmed_it
}
data2['y_p'] = np.diff(data2['y']) / np.diff(data2['x'])
data2['x_p'] = (np.array(data2['x'])[:-1] + np.array(data2['x'])[1:]) / 2


#plt.plot(confirmed.columns, np.log10(confirmed.loc['US']), label = 'US')
#plt.plot(confirmed.columns, np.log10(confirmed.loc['Sweden']), label = 'Sweden')
#plt.plot(confirmed.columns, np.log10(confirmed.loc['Italy']), label = 'Italy')

#plt.scatter(confirmed.columns[1:], data['y_p'], label = 'US')
plt.scatter(confirmed.columns[1:], data1['y_p'], label = 'Sweden')
plt.scatter(confirmed.columns[1:], data2['y_p'], label = 'Italy')

slope, intercept, r_value, p_value, std_err = stats.linregress(np.linspace(0, data1['y_p'].size, data1['y_p'].size), data1['y_p'])
predictions = np.linspace(0, data1['y_p'].size, data1['y_p'].size) * slope + intercept
plt.plot(np.linspace(0, data1['y_p'].size, data1['y_p'].size), predictions)


plt.axvline(dt.datetime(2020, 3, 9), color = 'green')
plt.axvline(dt.datetime(2020, 3, 19), color = 'blue')
plt.axvline(dt.datetime(2020, 4, 7), color = 'blue')
#plt.fill_between([dt.datetime(2020, 3, 19), dt.datetime(2020, 4, 7)], 35000, color='blue', alpha=0.1)
plt.legend()

# Set xaxis tick marks to be regular
years_fmt = mdates.DateFormatter('%Y-%m-%d')
plt.gca().xaxis.set_major_locator(plt.MultipleLocator(10))
plt.gca().xaxis.set_major_formatter(years_fmt)
plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(1))
plt.xlabel('Date')
plt.ylabel('Case Rate')
plt.title('Case Rate Over Time')

plt.show()

maxrateus = max(data['y_p'])
indmaxus = np.argmax(data['y_p'])
maxdateus = dates[indmaxus]

print('maxrate US: ' , maxrateus , ' on ' , maxdateus)

maxratesw = max(data1['y_p'])
indmaxsw = np.argmax(data1['y_p'])
maxdatesw = dates[indmaxsw]

print('maxrate SW: ' , maxratesw , ' on ' , maxdatesw)

maxrateit = max(data2['y_p'])
indmaxit = np.argmax(data2['y_p'])
maxdateit = dates[indmaxit]

print('maxrate IT: ' , maxrateit , ' on ' , maxdateit)