import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.dates as mdates

uscoviddata = pd.read_csv('dailyus.csv')

juststates = uscoviddata.drop(['date', 'positive', 'negative', 'pending',
       'hospitalizedCurrently', 'hospitalizedCumulative', 'inIcuCurrently',
       'inIcuCumulative', 'onVentilatorCurrently', 'onVentilatorCumulative',
       'recovered', 'dataQualityGrade', 'lastUpdateEt', 'hash', 'dateChecked',
       'death', 'hospitalized', 'total', 'totalTestResults', 'posNeg', 'fips',
       'deathIncrease', 'hospitalizedIncrease', 'negativeIncrease',
       'positiveIncrease', 'totalTestResultsIncrease'], axis=1)

justdates = uscoviddata.drop(['state', 'positive', 'negative', 'pending',
       'hospitalizedCurrently', 'hospitalizedCumulative', 'inIcuCurrently',
       'inIcuCumulative', 'onVentilatorCurrently', 'onVentilatorCumulative',
       'recovered', 'dataQualityGrade', 'lastUpdateEt', 'hash', 'dateChecked',
       'death', 'hospitalized', 'total', 'totalTestResults', 'posNeg', 'fips',
       'deathIncrease', 'hospitalizedIncrease', 'negativeIncrease',
       'positiveIncrease', 'totalTestResultsIncrease'], axis=1)

justpositive = uscoviddata.drop(['date', 'state', 'negative', 'pending',
       'hospitalizedCurrently', 'hospitalizedCumulative', 'inIcuCurrently',
       'inIcuCumulative', 'onVentilatorCurrently', 'onVentilatorCumulative',
       'recovered', 'dataQualityGrade', 'lastUpdateEt', 'hash', 'dateChecked',
       'death', 'hospitalized', 'total', 'totalTestResults', 'posNeg', 'fips',
       'deathIncrease', 'hospitalizedIncrease', 'negativeIncrease',
       'positiveIncrease', 'totalTestResultsIncrease'], axis=1)
#Below is a list that just has the state, date, and total positive cases.
#It is not useful in its current state
sdc = pd.concat([juststates,justdates,justpositive],axis=1)
#By setting the state code to be the indeces for the other columns we can do some easy stuff that gets rid of the rest of the cases to focus on one.
st_date_pos = sdc.set_index('state')

def data_for_state(statecode, df):
       data_ind = df.index == statecode
       new_df = df[data_ind]
       return new_df

def all_state(df):
       """the purpose of this code is to just prepare all the data for if you want to see it.
          It returns "states" which is just the list of state codes in the order that it appears in
          "df_states", which is a list of all the data frames that have dates and the number of
          total positive cases up to that date.
       """
       st_og = df.index.to_list()
       #next line removes duplicates from list
       states = list(set(st_og))
       df_states=[]
       all_data=[]
       for i in range(len(states)):
              df_states += [data_for_state(states[i], df)]
       return states, df_states

seperated_data = all_state(st_date_pos)
states = seperated_data[0]
df_states = seperated_data[1]

def plotcase(df):
       df['date'] = df['date'].apply(str)
       dates = df.date.to_list()
       cases = df.positive.to_list()
       cdates = dates[::-1]
       ccases = cases[::-1]
       
       plt.figure(figsize = (15,7))
       plt.xticks(rotation = 90)
       plt.gca().xaxis.set_major_locator(plt.MultipleLocator(5))
       plt.plot(cdates, ccases)
       plt.title('COVID19 Cases Over Time')
       plt.show()

def plottable(df):
       df['date'] = df['date'].apply(str)
       dates = df.date.to_list()
       cases = df.positive.to_list()
       #cdates = dates[::-1]
       #ccases = cases[::-1]
       return dates, cases


def plot_two(statecode1, statecode2, df):
       s1data = data_for_state(statecode1, df)
       s2data = data_for_state(statecode2, df)

       s1datecase=plottable(s1data)
       s2datecase=plottable(s2data)

       s1date=s1datecase[0]
       s1case=s1datecase[1]
       s2date=s2datecase[0]
       s2case=s2datecase[1]

       if len(s1date) < len(s2date):
              ruler = len(s2date) - len(s1date)
              to_add = len(s2date) - ruler
              s1date+=s2date[to_add:]
              for i in range(0, ruler):
                     s1case+=[0]
       else:
              ruler = len(s1date) - len(s2date)
              to_add = len(s1date) - ruler
              s2date+=s1date[to_add:]
              for i in range(0, ruler):
                     s2case+=[0]

       s1date=s1date[::-1]
       s1case=s1case[::-1]

       s2date=s2date[::-1]
       s2case=s2case[::-1]

       plt.figure(figsize = (15,7))
       plt.xticks(rotation = 90)
       plt.gca().xaxis.set_major_locator(plt.MultipleLocator(5))
       plt.plot(s1date, s1case, label = statecode1)
       plt.plot(s2date, s2case, label = statecode2)
       plt.legend()
       plt.title('COVID19 Cases Over Time')
       plt.show()

def plot_many(stateL, df):
       plt.figure(figsize = (15,7))
       plt.xticks(rotation = 90)
       plt.gca().xaxis.set_major_locator(plt.MultipleLocator(5))

       #got the data for WA because it has the most dates

       WA = data_for_state('WA', df)

       WA2 = plottable(WA)
       WAcase = WA2[1]
       WAdate = WA2[0]



       for i in range(len(stateL)):
              sdata = data_for_state(stateL[i], df)
              sdatecase = plottable(sdata)

              statecode = stateL[i]

              sdate = sdatecase[0]
              scase = sdatecase[1]
              #this process is used to make all the states have the same amount of cases
              ruler = len(WAdate) - len(sdate)
              to_add = len(WAdate) - ruler
              sdate+=WAdate[to_add:]
              #I figured that if the state didn't have any data for positive cases in those dates where nothing was reported, they would be zeros
              for i in range(0, ruler):
                     scase+=[0]

              #I reverse the dates and cases so that they go in chronological order
              #also, at this point, if you want to normalize the data or scale it or do anything, you can.
              #for example, you can log every entry in scase, however you must recognize that a lot of these case values are zero, so make sure to clean
              #that up however you want.

              udate = sdate[::-1]
              ucase = scase[::-1]

              plt.plot(udate, ucase, label = statecode)

       plt.legend()
       plt.title('COVID19 Cases Over Time')
       plt.show()

def scatter_many_derivative(stateL, df):
       plt.figure(figsize = (15,7))
       plt.xticks(rotation = 90)
       plt.gca().xaxis.set_major_locator(plt.MultipleLocator(5))

       WA = data_for_state('WA', df)
       WA2 = plottable(WA)
       WAcase = WA2[1]
       WAdate = WA2[0]
       for i in range(len(stateL)):
              sdata = data_for_state(stateL[i], df)
              sdatecase = plottable(sdata)
              statecode = stateL[i]
              sdate = sdatecase[0]
              scase = sdatecase[1]
              ruler = len(WAdate) - len(sdate)
              to_add = len(WAdate) - ruler
              sdate+=WAdate[to_add:]
              for i in range(0, ruler):
                     scase+=[0]
              udate = sdate[::-1]
              ucase = scase[::-1]

              xudate = range(len(udate))

              data = {
                     'x': xudate,
                     'y': ucase
              }

              data['y_p'] = np.diff(data['y']) / np.diff(data['x'])
              data['x_p'] = (np.array(data['x'])[:-1] + np.array(data['x'])[1:]) / 2

              plt.plot(udate[1:], data['y_p'], label = statecode)
       
       plt.xticks(rotation = 45)
       plt.fill_between(['20200319', '20200407'], 16000, 0, color='blue', alpha=0.1)
       #plt.legend()
       plt.xlabel('Date')
       plt.ylabel('Case Rate')
       plt.title('COVID19 Case Rate Over Time')
       plt.show()

def max_rate_date(stateL, df):
       max_rate = 0
       daterateL =[]

       WA = data_for_state('WA', df)
       WA2 = plottable(WA)
       WAcase = WA2[1]
       WAdate = WA2[0]
       for i in range(len(stateL)):
              sdata = data_for_state(stateL[i], df)
              sdatecase = plottable(sdata)
              statecode = stateL[i]
              sdate = sdatecase[0]
              scase = sdatecase[1]
              ruler = len(WAdate) - len(sdate)
              to_add = len(WAdate) - ruler
              sdate+=WAdate[to_add:]
              for i in range(0, ruler):
                     scase+=[0]
              udate = sdate[::-1]
              ucase = scase[::-1]

              xudate = range(len(udate))

              data = {
                     'x': xudate,
                     'y': ucase
              }

              data['y_p'] = np.diff(data['y']) / np.diff(data['x'])
              data['x_p'] = (np.array(data['x'])[:-1] + np.array(data['x'])[1:]) / 2

              maxrate = max(data['y_p'])
              indmax = np.argmax(data['y_p'])
              maxdate = udate[indmax]

              daterateL += [statecode, maxdate, maxrate]

       return daterateL





