#!/usr/bin/env python

import matplotlib
matplotlib.use('svg')
import matplotlib.dates as mdates
import pandas
import os
import time

hours = mdates.HourLocator(interval=6)

# read environment to connect to a remote mariaDB
__host__ = os.environ['DB_HOST']
__user__ = os.environ['DB_USER']
__passwd__ = os.environ['DB_PASSWD']
__db__ = os.environ['DB_DB']

df = pandas.read_sql_table("t28", "mysql://%s:%s@%s/%s" %
                           (__user__, __passwd__, __host__, __db__),
                           columns=['t', 'temperature'],
                           parse_dates={'t': 's'})
ds = pandas.Series(df['temperature'].values/1000.0, index=df['t'])
ds = ds.tz_localize('UTC').tz_convert('Europe/Berlin')
ds = ds.resample('H').mean()
ax = ds.plot(grid=True)
ax.set_title('Temperaturverlauf Dielheim, Kurpfalzstrasse 4')
ax.xaxis.set_minor_locator(hours)
matplotlib.pyplot.xlabel('Datum')
matplotlib.pyplot.ylabel('Temperatur in Grad Celsius')
matplotlib.pyplot.savefig("temperature%s.svg" % (str(time.time()),))
