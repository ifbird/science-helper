import os
import errno
import sys

import pandas as pd
import numpy as np
import numpy.ma as ma
from pyhdf.SD import *

from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

from tm5_parameters import tm5
from constants import *
import tools


"""
lrg : land reduced Gaussian
grg : global reduced Gaussian
nhrg: northern hemisphere reduced Gaussian
gg  : golbal Gaussian
g11 : global regular grid 1x1
g32 : global regular grid 3x2 (dlon x dlat)
"""

#==============================================================================#
#
# Global variables and parameters
#
#==============================================================================#
nlon_nhrg_N80 = tm5['nlon_N80']
lat_nhrg_N80 = tm5['lat_N80']

# Number of veg type
nvt = tm5['nvt']

# Number of months per year
nmon = 12

# nyear = 10


#==============================================================================#
#
# Helper function
#
#==============================================================================#
def print_debug(info, debug):
  if debug:
    print(info)


def read_data_rawpd(fname):
  """
  " Read from txt, delimiter is any space (' ' or '\t'), no header
  "
  " The data are saved in their original structure: (ngrid_lrg, n_columns)
  " The column names are saved in rawpd.columns
  """
  rawpd = pd.read_csv(fname, sep='\s+', header=None)
  
  # Set column names
  rawpd.columns = ['lon', 'lat', 'year'] + \
    ['lail{:02d}'.format(i+1) for i in range(nmon)] + \
    ['laih{:02d}'.format(i+1) for i in range(nmon)] + \
    ['cvl{:02d}'.format(i+1) for i in range(nmon)] + \
    ['cvh{:02d}'.format(i+1) for i in range(nmon)] + \
    ['vtl', 'vth']

  return rawpd


def read_data_lrg(fname):
  """
  " Organize the raw data to be easier for further processing
  "
  " lail, laih, cvl, cvh: (nyear, nmon, ngrid_lrg)
  " vtl, vth: (nyear, ngrid_lrg)
  " vtl_set, vth_set, vt_set: lists of the low, high and all vegetation types in number,
  "                           check tm5['veg_type']
  " tv: (nvt, nyear, ngrid_lrg), either 0 or 100 in Lu2018
  """
  # Read the raw pandas data
  rawpd = read_data_rawpd(fname)

  # Some parameters
  nyear = 10  # for simplicity
  nrow = len(rawpd.index)  # number of rows of raw data file, 10407*10
  ngrid_lrg = int(nrow/nyear)  # number of land grids, 10407

  # Set the data for reduced grid in land
  data_lrg = {}

  #
  # monthly mean LAI of low and high veg
  # 1850:
  #   12 months
  #   o o o ... o
  #   ...          ngrid_lrg (14070)
  #   o o o ... o
  # 1851:
  #   ...  similar with 1850
  #
  data_lrg['lail'] = np.transpose( np.reshape(rawpd.loc[:, 'lail01':'lail12'].values, (nyear, ngrid_lrg, nmon)), (0, 2, 1) )  # [year, mon, grid]
  data_lrg['laih'] = np.transpose( np.reshape(rawpd.loc[:, 'laih01':'laih12'].values, (nyear, ngrid_lrg, nmon)), (0, 2, 1) )  # [year, mon, grid]
  
  #
  # monthly mean coverage of low and high veg
  # The structure is similar with LAI
  #
  data_lrg['cvl'] = np.transpose( np.reshape(rawpd.loc[:, 'cvl01':'cvl12'].values, (nyear, ngrid_lrg, nmon)), (0, 2, 1) )  # [year, mon, grid]
  data_lrg['cvh'] = np.transpose( np.reshape(rawpd.loc[:, 'cvh01':'cvh12'].values, (nyear, ngrid_lrg, nmon)), (0, 2, 1) )  # [year, mon, grid]
  
  #
  # veg types, one type per year but may change interannually
  # ngrid_lrg
  # o o o ... o
  # ...         10 years
  # o o o ... o
  #
  data_lrg['vtl'] = np.reshape(rawpd.loc[:, 'vtl'].values, (nyear, ngrid_lrg))
  data_lrg['vth'] = np.reshape(rawpd.loc[:, 'vth'].values, (nyear, ngrid_lrg))
  
  # Find the set of low veg types
  vtl_set = np.unique(data_lrg['vtl'])  # low vegetation
  vtl_set = np.delete( vtl_set, np.argwhere(vtl_set == 0) )  # delete zero elements which means no veg
  data_lrg['vtl_set'] = vtl_set
  
  # Find the set of high veg types
  vth_set = np.unique(data_lrg['vth'])
  vth_set = np.delete( vth_set, np.argwhere(vth_set == 0) )
  data_lrg['vth_set'] = vth_set
  
  # Find the set of veg types
  vt_set = np.unique( np.concatenate((vtl_set, vth_set)) )  # all the vegetation types
  data_lrg['vt_set'] = vt_set
  
  #
  # percentage of each type from 01 to 20
  #
  data_lrg['tv'] = np.zeros((nvt, nyear, ngrid_lrg))
  
  # low veg
  for v in vtl_set:
    tv_ind = int(v-1)  # index is veg type minus 1
    data_lrg['tv'][tv_ind][ data_lrg['vtl'] == v ] = 100.0  # all veg belong to this low tv type
  
  # high veg
  for v in vth_set:
    tv_ind = int(v-1)  # index is veg type minus 1
    data_lrg['tv'][tv_ind][ data_lrg['vth'] == v ] = 100.0  # all veg belong to this high tv type

  # Grid information
  data_lrg['lon_lrg'], data_lrg['lat_lrg'] = rawpd['lon'][0:ngrid_lrg], rawpd['lat'][0:ngrid_lrg]

  # lon and lat in grg grid
  # data_lrg['lon_grg'], data_lrg['lat_grg'] = tools.calc_grg_grid(nlon_nhrg_N80, lat_nhrg_N80)

  # land indices (lrg grid) in grg grid
  # data_lrg['land_ind'] = tools.calc_land_ind_in_grg_grid( \
  #   data['lon_lrg'], data['lat_lrg'], data['lon_grg'], data['lat_grg'])
  return data_lrg


#==============================================================================#
#
# Classes
#
#==============================================================================#

class Lu2018():
  """
  "Dataset for the data used in Lu2018
  """

  #========================================#
  # Class variables
  #========================================#
  isset = False

  # Set to default none
  nyear = None
  ngrid_lrg = None
  lon_lrg, lat_lrg = None, None
  lon_grg, lat_grg = None, None
  land_ind = None
  lon_g11, lat_g11 = None, None
  lon_g32, lat_g32 = None, None


  #========================================#
  # Class methods
  #========================================#
  @classmethod
  def set_class_vars(cls, nyear, ngrid_lrg, lon_lrg, lat_lrg):
    cls.nyear = nyear
    cls.ngrid_lrg = ngrid_lrg

    # lon and lat in lrg grid
    cls.lon_lrg, cls.lat_lrg = lon_lrg, lat_lrg

    # lon and lat in grg grid
    cls.lon_grg, cls.lat_grg = tools.calc_grg_grid(nlon_nhrg_N80, lat_nhrg_N80)

    # land indices (lrg grid) in grg grid
    cls.land_ind = tools.calc_land_ind_in_grg_grid(cls.lon_lrg, cls.lat_lrg, cls.lon_grg, cls.lat_grg)

    # Global regular grids, west --> east, south --> north
    xbeg, xend = -180, 180
    ybeg, yend = -90, 90

    dlon, dlat = 1.0, 1.0
    cls.lon_g11, cls.lat_g11 = tools.calc_gxx_grid(xbeg, xend, dlon, ybeg, yend, dlat)

    dlon, dlat = 3.0, 2.0
    cls.lon_g32, cls.lat_g32 = tools.calc_gxx_grid(xbeg, xend, dlon, ybeg, yend, dlat)

    # Set it to true to avoid repeating
    cls.isset = True


  #========================================#
  # Static methods
  #========================================#


  #========================================#
  # Instance methods
  #========================================#
  def __init__(self, fname):
    """
    Raw data structure:
    x: lon | lat | year | lail01-laih12 | laih01-laih12 | cvl01-cvl12 | cvh01-cvh12 | vtl | vth
    y: all the land grid, loop for each year

    lon, lat: the same for each year
    year: 1850 - 1859, I do not know why it is the same for MH and MHgsrd

    lail, laih, cvl, cvh: [nyear*ngrid_lrg, nmon] --> [nyear, nmon, ngrid_lrg]
    vtl, vth: [nyear*ngrid_lrg] --> [nyear, ngrid_lrg]
    """

    # Read raw data from file fname in pandas dataframe format
    rawpd = read_data_rawpd(fname)
  
    nyear = 10  # for simplicity
    nrow = len(rawpd.index)  # number of rows of raw data file, 10407*10
    ngrid_lrg = int(nrow/nyear)  # number of land grids, 10407

    # Set class variables
    if not Lu2018.isset:
      Lu2018.set_class_vars(nyear, ngrid_lrg, rawpd['lon'][0:ngrid_lrg], rawpd['lat'][0:ngrid_lrg])

    # Read data_lrg
    self.data_lrg = read_data_lrg(fname)


  def calc_data_gxx(self, lon_gxx, lat_gxx, debug=False):
    """
    " Get data_gxx from self.data_lrg
    """

    # Set parameters
    nyear = Lu2018.nyear
    ngrid_lrg = Lu2018.ngrid_lrg

    lon_lrg, lat_lrg = Lu2018.lon_lrg, Lu2018.lat_lrg
    land_ind = Lu2018.land_ind
    lon_grg, lat_grg = Lu2018.lon_grg, Lu2018.lat_grg

    nlon_gxx, nlat_gxx = lon_gxx.size, lat_gxx.size

    vtl_set, vth_set = self.data_lrg['vtl_set'], self.data_lrg['vth_set']

    # Calculate data_grg
    data_gxx = {}

    # Add new coordinates to data_gxx
    data_gxx['lon'], data_gxx['lat'] = lon_gxx, lat_gxx

    # Interpolation is linear for lail, laih, cvl, and cvh
    # [year, mon, grid] --> [year, mon, lon_gxx, lat_gxx]
    for v in ['lail', 'laih', 'cvl', 'cvh']:
      # Debug info
      print_debug('Interpolating {0} ...'.format(v), debug)

      # Init
      data_gxx[v] = np.zeros( (nyear, nmon, nlon_gxx, nlat_gxx) )

      # Interpolate for each month in every year
      for iy in range(nyear):
        # Debug info
        print_debug('Year number {0} ...'.format(iy), debug)

        for im in range(nmon):
          # Debug info
          # print_debug('Month {0} ...'.format(im+1), debug)

          data_gxx[v][iy, im][:, :] = \
              tools.data_lrg2gxx(self.data_lrg[v][iy, im, :], \
              lon_lrg, lat_lrg, land_ind, \
              lon_grg, lat_grg, \
              lon_gxx, lat_gxx, \
              kind='linear')

    # Interpolation is nearest for vtl, vth
    # [year, grid] --> [year, lon_gxx, lat_gxx]
    for v in ['vtl', 'vth']:
      # Debug info
      print_debug('Interpolating {0} ...'.format(v), debug)

      # Init
      data_gxx[v] = np.zeros( (nyear, nlon_gxx, nlat_gxx) )

      # Interpolate for each month in every year
      for iy in range(nyear):
        # Debug info
        # print_debug('Year number {0} ...'.format(iy), debug)

        data_gxx[v][iy][:, :] = \
            tools.data_lrg2gxx(self.data_lrg[v][iy, :], \
            lon_lrg, lat_lrg, land_ind, \
            lon_grg, lat_grg, \
            lon_gxx, lat_gxx, \
            kind='nearest')

    # Set tv according to vtl and vth
    # Here we do not interpolate tv to save time

    # Init
    data_gxx['tv'] = np.zeros( (nvt, nyear, nlon_gxx, nlat_gxx) )
    # low veg
    for v in vtl_set:
      tv_ind = int(v-1)  # index is veg type minus 1
      mask = data_gxx['vtl'] == v
      data_gxx['tv'][tv_ind][mask] = 100.0  # all veg belong to this low tv type

    # high veg
    for v in vth_set:
      tv_ind = int(v-1)  # index is veg type minus 1
      mask = data_gxx['vth'] == v
      data_gxx['tv'][tv_ind][mask] = 100.0  # all veg belong to this high tv type

    self.data_gxx = data_gxx

    return data_gxx



#===========================================================================#
#
# Old style to process the data#
#
#===========================================================================#
def lu2018_process_rawpd_to_cook(rawpd):
  """
  lon, lat: the same for each year
  year: 1850 - 1859, I do not know why it is the same for MH and MHgsrd
  lail, laih, cvl, cvh: [nyear*ngrid, nmon] --> [nyear, nmon, ngrid]
  vtl, vth: [nyear*ngrid] --> [nyear, ngrid]
  """
  
  nyear = 10  # 10-year data
  nrow = len(rawpd.index)  # number of rows of raw data file, 10407*10
  ngrid = int(nrow/nyear)  # number of land grids, 10407
  
  # Initiate the data dict
  cook = {}

  # number of year
  cook['nyear'] = nyear

  # number of land grids
  cook['ngrid'] = ngrid

  # longitude and latitude
  cook['lon'] = rawpd['lon'][0:ngrid]
  cook['lat'] = rawpd['lat'][0:ngrid]

  #
  # monthly mean LAI of low and high veg
  # 1850:
  #   12 months
  #   o o o ... o
  #   ...          ngrid (14070)
  #   o o o ... o
  # 1851:
  #   ...  similar with 1850
  #
  cook['lail'] = np.transpose( np.reshape(rawpd.loc[:, 'lail01':'lail12'].values, (nyear, ngrid, nmon)), (0, 2, 1) )  # [year, mon, grid]
  cook['laih'] = np.transpose( np.reshape(rawpd.loc[:, 'laih01':'laih12'].values, (nyear, ngrid, nmon)), (0, 2, 1) )  # [year, mon, grid]
  
  #
  # monthly mean coverage of low and high veg
  # The structure is similar with LAI
  #
  cook['cvl'] = np.transpose( np.reshape(rawpd.loc[:, 'cvl01':'cvl12'].values, (nyear, ngrid, nmon)), (0, 2, 1) )  # [year, mon, grid]
  cook['cvh'] = np.transpose( np.reshape(rawpd.loc[:, 'cvh01':'cvh12'].values, (nyear, ngrid, nmon)), (0, 2, 1) )  # [year, mon, grid]
  
  #
  # veg types, one type per year but may change interannually
  # ngrid
  # o o o ... o
  # ...         10 years
  # o o o ... o
  #
  cook['vtl'] = np.reshape(rawpd.loc[:, 'vtl'].values, (nyear, ngrid))
  cook['vth'] = np.reshape(rawpd.loc[:, 'vth'].values, (nyear, ngrid))
  
  return cook


def lu2018_further_process_cook(cook):
  # Set parameters
  nyear = cook['nyear']
  ngrid = cook['ngrid']
  
  #####
  # Find the the most frequent veg type during 10 years
  # So finally, for each grid, there is only one dominant type within 10 years
  #####
  
  # Set the initial data, each grid only has one dominant vegetation type during 10 years
  cook['vtl_dom'] = np.zeros((ngrid,))
  cook['vth_dom'] = np.zeros((ngrid,))
  
  # Set the type bins to trap the numbers from 0 to 20
  bins = np.arange(-0.5, 21, 1)
  
  # Loop for each grid
  for i in range(ngrid):
    # Find the distribution of low types during 10 years
    hist_l, _bins = np.histogram(cook['vtl'][:, i], bins)
  
    # Find all the dominant types
    dominant_l_all = np.argwhere( hist_l == np.amax(hist_l) ).flatten()  # the indices of most frequent veg
  
    # If the dominant types are more than one, the last occurred one is considered dominant
    if dominant_l_all.size > 1:
      ilast = []
      for d in dominant_l_all:
        ilast.append( np.argwhere(cook['vtl'][::-1, i] == d).flatten()[0] )  # the last occurence
      i1 = np.argmin(ilast)  # who occurs the last, notice the array is reversed
      cook['vtl_dom'][i] = dominant_l_all[i1]
    # Just use the value if only one dominant type
    else:
      cook['vtl_dom'][i] = dominant_l_all[0]
  
      # Do the same for high veg
  
    # Find the distribution of high types during 10 years
    hist_h, _bins = np.histogram(cook['vth'][:, i], bins)
  
    # Find all the dominant types
    dominant_h_all = np.argwhere( hist_h == np.amax(hist_h) ).flatten()  # the indices of most frequent veg
  
    # If the dominant types are more than one, the last occurred one is considered dominant
    if dominant_h_all.size > 1:
      ilast = []
      for d in dominant_h_all:
        ilast.append( np.argwhere(cook['vth'][::-1, i] == d).flatten()[0] )  # the last occurence
      i1 = np.argmin(ilast)  # who occurs the last, notice the array is reversed
      cook['vth_dom'][i] = dominant_h_all[i1]
    # Just use the value if only one dominant type
    else:
      cook['vth_dom'][i] = dominant_h_all[0]
  
    #####
    #Calculate the 10 year monthly averaged vegetation coverage for each grid at each month
    # The dominant vegetation type is used.
    # ngrid
    # o o o ... o
    # ...          12 months
    # o o o ... o
    #####
    cook['cvl_dom_avg'] = np.zeros((nmon, ngrid))
    cook['cvh_dom_avg'] = np.zeros((nmon, ngrid))
  
    for i in range(ngrid):
      # Find the year indices of the dominant low veg type
      mask = cook['vtl'][:, i] == cook['vtl_dom'][i]
      cook['cvl_dom_avg'][:, i] = np.mean( cook['cvl'][mask, :, i], axis=0)
  
      # Find the year indices of the dominant high veg type
      mask = cook['vth'][:, i] == cook['vth_dom'][i]
      cook['cvh_dom_avg'][:, i] = np.mean( cook['cvh'][mask, :, i], axis=0)
  
    # 10-year veg type, [ngrid]
    cook['vtl_10a_avg'] = np.mean(cook['vtl'], axis=0)
    cook['vth_10a_avg'] = np.mean(cook['vth'], axis=0)
  
    #####
    # Set of veg types
    #####
    # Find the set of low veg types
    vtl_set = np.unique(cook['vtl'])  # low vegetation
    vtl_set = np.delete( vtl_set, np.argwhere(vtl_set == 0) )  # delete zero elements which does not make sense
  
    # Find the set of high veg types
    vth_set = np.unique(cook['vth'])
    vth_set = np.delete( vth_set, np.argwhere(vth_set == 0) )
  
    # Find the set of veg types
    vt_set = np.unique( np.concatenate((vtl_set, vth_set)) )  # all the vegetation types
  
    cook['vtl_set'] = vtl_set
    cook['vth_set'] = vth_set
    cook['vt_set']  = vt_set
  
    #####
    # Get the coverage for each veg type on land.
    # This is an extension and combination of data['cvl'] and data['cvh'].
    # cvl, cvh: the veg types are not separated
    # cv: every veg type has a complete dataset on land grid
    #
    # Data structure of cv_dom:
    # tv##: the veg types, from 1 to 20
    # tv01
    # o o o ... o
    # ...          12 months
    # o o o ... o
    # tv02
    # o o o ... o
    # ...          12 months
    # o o o ... o
    #####
  
    # cv_dom
    cook['cv_dom'] = np.zeros((nvt, nmon, ngrid))
    for v in vtl_set:
      mask = cook['vtl_dom'] == v
      cook['cv_dom'][int(v-1)][:, mask] = cook['cvl_dom_avg'][:, mask]
  
    for v in vth_set:
      mask = cook['vth_dom'] == v
      cook['cv_dom'][int(v-1)][:, mask] = cook['cvh_dom_avg'][:, mask]
  
    # Get tv_dom, either 0 or 100, each grid should have only one value for each year.
    cook['tv_dom'] = np.zeros((nvt, ngrid))
    for v in vtl_set:
      mask = cook['vtl_dom'][:] == v
      # Use a mixing of basic and advanced indexing to prevent shape error
      cook['tv_dom'][int(v-1), mask] = 100.0  # in LPJG, only one vegetation can exist for low type
  
    for v in vth_set:
      mask = cook['vth_dom'][:] == v
      # Use a mixing of basic and advanced indexing to prevent shape error
      cook['tv_dom'][int(v-1), mask] = 100.0  # in LPJG, only one vegetation can exist for high type
    
    return cook
  
  
# Test
if __name__ == "__main__":
  pass
  
