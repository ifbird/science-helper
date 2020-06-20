#==============================================================================#
#
# Readme
#
# In puhti, we can load python env then run the code:
# $ module load python-env/2019.3
#
#==============================================================================#

import os
import sys
import re
# import json

import datetime

import numpy as np
import pandas as pd
import xarray as xr

# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import matplotlib.dates as mdt
# from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange

# import functions as fcn
# import ptpack.parameter as ppp


#==============================================================================#
#
# Help functions
#
#==============================================================================#

#---------------------------------------------------------#
# Check if a file exists
#---------------------------------------------------------#

def file_exist(file_abs_path):
  return os.path.isfile(file_abs_path)

#---------------------------------------------------------#
# Convert date array with 6 numbers for datetime
# (second with decimals) to datetime list
#---------------------------------------------------------#
def datearray_to_datetimelist(date6):
  """
  " Convert date array with 6 numbers for datetime (second with decimals) to datetime list
  """
  nt = date6.shape[0]  # number of time steps
  dtlst = np.array([None]*nt)
  date7_temp = np.zeros((7,))
  for it in range(nt):
    date7_temp[0:6] = date6[it,:]
    date7_temp[6] = (date6[it, 5]-np.fix(date6[it, 5]))*1e6  # get microseconds
    date7_temp[5] = np.fix(date6[it, 5])  # get seconds
    dtlst[it] = datetime.datetime(*date7_temp.astype(int))

  return (nt, dtlst)

#---------------------------------------------------------#
# Print a dictionary recursively
#---------------------------------------------------------#
def print_dict(f, myDict, prefix=''):
  prefix += '  '
  for k, v in myDict.iteritems():
    if isinstance(v, dict):
      f.write('{0}{1}\n'.format(prefix, k))
      print_dict(f, v, prefix)
    else:
      if type(v).__module__ == np.__name__:  # if v is a numpy array
        f.write('{p}{k}: {v}\n'.format(p=prefix, k=k, v=v.shape))
      else:
        f.write('{p}{k}: {v}\n'.format(p=prefix, k=k, v=v))


#==============================================================================#
#
# Class definition
#
#==============================================================================#

#---------------------------------------------------------#
# SOSAA data pack for netcdf files
#---------------------------------------------------------#
class SosaaNc:
  def __init__(self, folder='.'):
    # Obtain data folder
    self.folder = folder

    #
    # Initiate xarray dataset
    #

    # meteo data
    meteo_file_name = self.folder + '/meteo.nc'
    xrds_meteo = xr.open_dataset(meteo_file_name)

    # chem data
    chem_file_name  = self.folder + '/chem.nc'
    xrds_chem  = xr.open_dataset(chem_file_name)

    # Merge the datasets
    self.xrds = xr.merge([xrds_meteo, xrds_chem])


#---------------------------------------------------------#
# SOSAA data pack for dat files
#---------------------------------------------------------#
class SosaaDat:
  var_file_dict = {
    'ua': 'UUU.dat',
    'va': 'VVV.dat',
    'temp': 'TEMP.dat',
    'tke': 'TKE.dat',
    'nconc_OH': 'Gas_OH.dat',
    'nconc_APINENE': 'Gas_APINENE.dat',
    'nconc_BPINENE': 'Gas_BPINENE.dat',
    }

  def __init__(self, folder='.'):
    # Obtain data folder
    self.folder = folder

    # Initiate xarray dataset
    self.xrds = xr.Dataset()


  def get_dimensions(self):
    # time, read from file
    time, _ = self.read_data_from_file('UUU.dat', True)

    # lev, set manually
    lev = np.array([ \
      0.0, 0.17, 0.38, 0.62, 0.90, \
      1.23, 1.61, 2.07, 2.60, 3.23, \
      3.96, 4.82, 5.83, 7.02, 8.41, \
      10.04, 11.96, 14.21, 16.86, 19.96, \
      23.60, 27.87, 32.88, 38.76, 45.67, \
      53.77, 63.28, 74.45, 87.55, 102.93, \
      120.98, 142.16, 167.02, 196.20, 230.44, \
      270.63, 317.81, 373.17, 438.15, 514.41, \
      603.92, 708.97, 832.26, 976.97, 1146.80, \
      1346.13, 1580.07, 1854.64, 2176.89, 2555.11, \
      3000.00 \
      ])

    self.xrds.coords['time'] = ('time', time)
    self.xrds.coords['lev'] = ('lev', lev)


  def get_variables_from_file(self, var_name, dims, file_name):
    file_abs_path = self.get_file_abs_path(file_name)
    if file_exist(file_abs_path):
      _, var = self.read_data_from_file(file_name)
      self.xrds[var_name] = ( dims, var )
    else:
      print('{0} does not exist.'.format(file_abs_path))
      self.xrds[var_name] = None


  def read_data_from_file(self, file_name, read_time=False):
    """
    " Read the output file,
    " save data to var_name:
    "   data_raw: raw data, maybe later the 30-min average data will also be added
    "   time_raw: raw time, represented by datetime.datetime numpy array
    """
    # Read time and data
    temp = np.genfromtxt(self.folder+'/'+file_name)
    data_raw = temp[:,6:].copy()
    if read_time:
      time_raw = np.array([datetime.datetime(*(temp[i,0:6].astype(int))) for i in range(temp.shape[0])])
    else:
      time_raw = np.array([])

    return (time_raw, data_raw)


  def get_file_abs_path(self, file_name):
    return self.folder + '/' + file_name


  def print_help(self, helpFile):
    with open(helpFile, 'w') as f:
      f.write('{0:10s}: {1}\n'.format('folder', self.folder))
      f.write('{0:10s}: {1}\n'.format('data file', self.dataFile))
      print_dict(f, self.data)


class SosaaCase():
  def __init__(self):
    pass
