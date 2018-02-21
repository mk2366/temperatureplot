#!/usr/bin/env python

import matplotlib
matplotlib.use('svg')
import matplotlib.pyplot
import matplotlib.dates as mdates
import pandas
import os
import time
import datetime
from dateutil import tz

timezone = tz.tzlocal()

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

f = matplotlib.pyplot.gcf()
f.set_size_inches(12.8, 19.2)

matplotlib.pyplot.subplot(311)
ax = ds.plot(grid=True)
ax.set_title('Temperaturverlauf Dielheim, Kurpfalzstrasse 4, Epoche')
matplotlib.pyplot.xlabel('Datum')
matplotlib.pyplot.ylabel('Temperatur in Grad Celsius')

matplotlib.pyplot.subplot(312)

now = datetime.datetime.now(timezone)
eightyfourhours = datetime.timedelta(hours=48)
sevendays = datetime.timedelta(days=7)

ax = ds[ds.index >= (now - eightyfourhours)].plot(grid=True)
ax.set_title('Temperaturverlauf Dielheim, Kurpfalzstrasse 4, 48 Stunden')
ax.xaxis.set_minor_locator(hours)
matplotlib.pyplot.xlabel('Datum')
matplotlib.pyplot.ylabel('Temperatur in Grad Celsius')

matplotlib.pyplot.subplot(313)
ax = ds[ds.index >= (now - sevendays)].plot(grid=True)
ax.set_title('Temperaturverlauf Dielheim, Kurpfalzstrasse 4, 7 Tage')
matplotlib.pyplot.xlabel('Datum')
matplotlib.pyplot.ylabel('Temperatur in Grad Celsius')

matplotlib.pyplot.tight_layout()

# matplotlib.pyplot.savefig("temperature%s.svg" % (str(time.time()),), dpi=200)
# matplotlib.pyplot.savefig("temp.svg", dpi=200)
matplotlib.pyplot.savefig("temp.png", dpi=200)
