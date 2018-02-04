#!/usr/bin/env python

import matplotlib
matplotlib.use('svg')
import pandas
import os
import time

# read environment to connect to a remote mariaDB
__host__ = os.environ['DB_HOST']
__user__ = os.environ['DB_USER']
__passwd__ = os.environ['DB_PASSWD']
__db__ = os.environ['DB_DB']

df = pandas.read_sql_table("t28","mysql://%s:%s@%s/%s" %
                      (__user__, __passwd__, __host__, __db__))
df = df.drop('user',1)
df = df.drop('id',1)
df['t'] = pandas.to_datetime(df.t, unit='s')
ds = pandas.Series(df['temperature'].values, index=df['t'])
ds = ds.tz_localize('UTC').tz_convert('Europe/Berlin')
ds = ds.resample('H').mean()
ds.plot()
matplotlib.pyplot.savefig("temperature%s.svg" % (str(time.time()),))
