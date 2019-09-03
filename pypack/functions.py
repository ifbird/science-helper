#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Header
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
import os
import sys

import re

import datetime
import calendar

import numpy as np
import scipy.interpolate as interpolate
import netCDF4 as netcdf

# import matplotlib as mpl
# mpl.use('Agg')
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import axes3d

from .parameters import *


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Set parameters
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# Functions
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def read_avaa(fname, vnames, database='HYY_META'):
  if type(vnames) is list:  # make sure vnames is a list
    vnames_new = vnames
  else:
    vnames_new = [vnames]

  csv_data = np.genfromtxt(fname, delimiter=',', names=True, deletechars="")  # keep the column names as they are
  data = {}

  for v in vnames_new:
    data[v] = None  # Set to None if not found in the file

    if v == 'time':  # save time as datetime array
      nt = csv_data['Year'].size
      data[v] = np.array([None]*nt)
      for i in range(nt):
        data[v][i] = datetime.datetime(int(csv_data['Year'][i]), int(csv_data['Month'][i]), int(csv_data['Day'][i]), \
          int(csv_data['Hour'][i]), int(csv_data['Minute'][i]), int(csv_data['Second'][i]))
    else:  # save other variables
      for vcol in csv_data.dtype.names:
        regex = r'\.' + re.escape(v) + r'$'  # column names are like: HYY_META.Net, HYY_META.Glob
        m = re.search(regex, vcol)
        if m:
          data[v] = csv_data[vcol]
          break

  return data


def read_profile(fname, vname):
  # Check if the vname exists
  found = False

  # Open the file
  with open(fname) as f:
    # Search the var name in the file
    for line in f:
      # if line.find(vname) != -1:  # if the var name is found, break and read next line
      if re.match(r'\b'+vname+r'\b', line):  # if the var name is found, break and read next line
        found = True
        break

    if found:
      # Get the var dimension
      line = next(f)  # read next line
      vshape = np.array(line.split()).astype('int')  # obtain the var dimension

      # Initiate var array
      var = np.zeros(vshape)

      # Read data from next line
      next(f)
      for i, line in enumerate(f):
        if i >= vshape[0]:  # read the data with known dimension
          break
        else:
          var[i, :] = np.array(line.split()).astype('float')

      return var
    else:  # the var is not found
      return None


def read_netcdf_data(fname, vname):
  fid = netcdf.Dataset(fname, mode='r')

  # Read variable, note that scale_factor and add_offset are considered already in netCDF4
  var_obj = fid.variables[vname]
  var = np.ma.filled(var_obj[:], fill_value=np.nan)  # masked array to numpy array with setting fill values to np.nan
  
  # Read time
  time_obj = fid.variables['time']
  time = netcdf.num2date(time_obj[:], units=time_obj.units, calendar=time_obj.calendar)  # convert to datetime type
  
  # Read latitude, longitude and level
  lat = fid.variables['latitude'][::-1]  # latitude is saved from north to south, so here I have reversed it
  lon = fid.variables['longitude'][:]
  if 'level' in fid.variables.keys():  # pressure levels
    lev = fid.variables['level'][:]
  else:  # only surface
    lev = -1
  
  return var, time, lev, lat, lon


