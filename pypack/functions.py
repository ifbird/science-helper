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
import xarray as xr

# import matplotlib as mpl
# mpl.use('Agg')
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import axes3d

# from .parameters import *


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


"""
" Masked average with or without weights
"
" mask, weights: masked weighted
" mask: masked average
" weights: weighted
"
" Examples:
" 1. Global weighted average
"   aw_xr = areacella['areacella']
"   glob_mean = masked_average(tas_ds['tas'], dim=['lat','lon'], weights=aw_xr)
"
" 2. Weighted average in arctic region
"   aw_xr = areacella['areacella']
"   mask = tas_ds['lat']<60.  # mask values with lat < 60 deg north
"   glob_mean = masked_average(tas_ds['tas'], dim=['lat','lon'], weights=aw_xr, mask=mask)
"
" Refer to:
" https://nordicesmhub.github.io/NEGI-Abisko-2019/training/Example_model_global_arctic_average.html
"""
def masked_average(xa:xr.DataArray,
                   dim=None,
                   weights:xr.DataArray=None,
                   mask:xr.DataArray=None):
    """
    This function will average
    :param xa: dataArray
    :param dim: dimension or list of dimensions. e.g. 'lat' or ['lat','lon','time']
    :param weights: weights (as xarray)
    :param mask: mask (as xarray), True where values to be masked.
    :return: masked average xarray
    """
    #lest make a copy of the xa
    xa_copy:xr.DataArray = xa.copy()

    if mask is not None:
        xa_weighted_average = __weighted_average_with_mask(
            dim, mask, weights, xa, xa_copy
        )
    elif weights is not None:
        xa_weighted_average = __weighted_average(
            dim, weights, xa, xa_copy
        )
    else:
        xa_weighted_average =  xa.mean(dim)

    return xa_weighted_average


def __weighted_average(dim, weights, xa, xa_copy):
    '''helper function for masked_average'''
    _, weights_all_dims = xr.broadcast(xa, weights)  # broadcast to all dims
    x_times_w = xa_copy * weights_all_dims
    xw_sum = x_times_w.sum(dim)
    x_tot = weights_all_dims.where(xa_copy.notnull()).sum(dim=dim)
    xa_weighted_average = xw_sum / x_tot
    return xa_weighted_average


def __weighted_average_with_mask(dim, mask, weights, xa, xa_copy):
    '''helper function for masked_average'''
    _, mask_all_dims = xr.broadcast(xa, mask)  # broadcast to all dims
    xa_copy = xa_copy.where(np.logical_not(mask))
    if weights is not None:
        _, weights_all_dims = xr.broadcast(xa, weights)  # broadcast to all dims
        weights_all_dims = weights_all_dims.where(~mask_all_dims)
        x_times_w = xa_copy * weights_all_dims
        xw_sum = x_times_w.sum(dim=dim)
        x_tot = weights_all_dims.where(xa_copy.notnull()).sum(dim=dim)
        xa_weighted_average = xw_sum / x_tot
    else:
        xa_weighted_average = xa_copy.mean(dim)
    return xa_weighted_average
