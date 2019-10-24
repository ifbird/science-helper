import os
import errno
import sys

import pandas as pd
import numpy as np
import numpy.ma as ma
from scipy import interpolate
from pyhdf.SD import *

from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
# mpl.use('Agg')
import matplotlib.pyplot as plt

import putian_functions as pf


#
# Some parameters
#

DPI = 150

# Number of veg type
nvt = 20

# Number of months per year
nmon = 12

# Case list
clist = ['pi', 'mh', 'mg']

# The grid in Lu2018 lpjg dataset is in N80 Gaussian grids with T159 resolution,
# the grid table can be checked below:
# * https://artefacts.ceda.ac.uk/badc_datadocs/ecmwf-op/grids.html#t159
# * https://rda.ucar.edu/datasets/common/ecmwf/ERA40/docs/std-transformations/dss_code_glwp.html

# Gaussian latitudes for N80 (T159, nlon=320 at equator) on nothern hemisphere
lat_N80 = np.array([ \
  89.1416, 88.0294, 86.9108, 85.7906, 84.6699, \
  83.5489, 82.4278, 81.3066, 80.1853, 79.0640, \
  77.9426, 76.8212, 75.6998, 74.5784, 73.4570, \
  72.3356, 71.2141, 70.0927, 68.9712, 67.8498, \
  66.7283, 65.6069, 64.4854, 63.3639, 62.2425, \
  61.1210, 59.9995, 58.8780, 57.7566, 56.6351, \
  55.5136, 54.3921, 53.2707, 52.1492, 51.0277, \
  49.9062, 48.7847, 47.6632, 46.5418, 45.4203, \
  44.2988, 43.1773, 42.0558, 40.9343, 39.8129, \
  38.6914, 37.5699, 36.4484, 35.3269, 34.2054, \
  33.0839, 31.9624, 30.8410, 29.7195, 28.5980, \
  27.4765, 26.3550, 25.2335, 24.1120, 22.9905, \
  21.8690, 20.7476, 19.6261, 18.5046, 17.3831, \
  16.2616, 15.1401, 14.0186, 12.8971, 11.7756, \
  10.6542,  9.5327,  8.4112,  7.2897,  6.1682, \
   5.0467,  3.9252,  2.8037,  1.6822,  0.5607, \
  ])

# Longitude points at each latitude for reduced Gaussian grids
nlon_N80 = np.array([ \
   18,  25,  36,  40,  45,  54,  60,  64,  72,  72, \
   80,  90,  96, 100, 108, 120, 120, 128, 135, 144, \
  144, 150, 160, 160, 180, 180, 180, 192, 192, 200, \
  200, 216, 216, 216, 225, 225, 240, 240, 240, 256, \
  256, 256, 256, 288, 288, 288, 288, 288, 288, 288, \
  288, 288, 300, 300, 300, 300, 320, 320, 320, 320, \
  320, 320, 320, 320, 320, 320, 320, 320, 320, 320, \
  320, 320, 320, 320, 320, 320, 320, 320, 320, 320, \
  ])

tm5_veg_type = { \
  'tv01': ('Crops, mixed farming'      , 'L'), \
  'tv02': ('Short grass'               , 'L'), \
  'tv03': ('Evergreen needleleaf trees', 'H'), \
  'tv04': ('Deciduous needleleaf trees', 'H'), \
  'tv05': ('Deciduous broadleaf trees' , 'H'), \
  'tv06': ('Evergreen broadleaf trees' , 'H'), \
  'tv07': ('Tall grass'                , 'L'), \
  'tv08': ('Desert'                    , '-'), \
  'tv09': ('Tundra'                    , 'L'), \
  'tv10': ('Irrigated crops'           , 'L'), \
  'tv11': ('Semidesert'                , 'L'), \
  'tv12': ('Ice caps and glaciers'     , '-'), \
  'tv13': ('Bogs and marshes'          , 'L'), \
  'tv14': ('Inland water'              , '-'), \
  'tv15': ('Ocean'                     , '-'), \
  'tv16': ('Evergreen shrubs'          , 'L'), \
  'tv17': ('Deciduous shrubs'          , 'L'), \
  'tv18': ('Mixed forest/woodland'     , 'H'), \
  'tv19': ('Interrupted forest'        , 'H'), \
  'tv20': ('Water and land mixtures'   , 'L'), \
  'cvh' : 'High vegetation cover', \
  'cvl' : 'Low vegetation cover' , \
  }

tm5_tvname = ['tv{:02d}'.format(int(i)) for i in range(1, nvt+1)]

tm5_vtname = [ \
  'Crops, mixed farming'      , \
  'Short grass'               , \
  'Evergreen needleleaf trees', \
  'Deciduous needleleaf trees', \
  'Deciduous broadleaf trees' , \
  'Evergreen broadleaf trees' , \
  'Tall grass'                , \
  'Desert'                    , \
  'Tundra'                    , \
  'Irrigated crops'           , \
  'Semidesert'                , \
  'Ice caps and glaciers'     , \
  'Bogs and marshes'          , \
  'Inland water'              , \
  'Ocean'                     , \
  'Evergreen shrubs'          , \
  'Deciduous shrubs'          , \
  'Mixed forest/woodland'     , \
  'Interrupted forest'        , \
  'Water and land mixtures'   , \
  ]

tm5_veglh = [ \
  'L', 'L', 'H', 'H', 'H', \
  'H', 'L', '-', 'L', 'L', \
  'L', '-', 'L', '-', '-', \
  'L', 'L', 'H', 'H', 'L', \
  ]

# 999 means not available
tm5_cveg = np.array([ \
  0.9 , 0.85, 0.9, 0.9, 0.9, \
  0.99, 0.7 , 0.0, 0.5, 0.9, \
  0.1 , 999 , 0.6, 999, 999, \
  0.5 , 0.5 , 0.9, 0.9, 0.6, \
  ])

tm5_veg_low  = np.array([1, 2, 7, 9, 10, 11, 13, 16, 17, 20])
tm5_veg_high = np.array([3, 4, 5, 6, 18, 19])

lu2018_veg_low = np.array([2, 7, 9, 13])
lu2018_veg_high = np.array([3, 4, 5, 6, 18])

# Region parameters
reg_glob = (-90, 90, -180, 180)  # global
reg_wafr = ( -5, 40,  -20,  50)  # west Africa defined in Lu2018
reg_sahara = ( 10, 30,  -20,  40)  # Sahara region in Ergerer2018


# def get_lat_lon_reduced_gaussian(lat, nlon):
#   # Number of all latitudes
#   nlat = 2 * lat.size
#   lat = np.zeros((nlat,))
#   lon = np.zeros((nlat, 


def set_dir(d):
  """
  " Create a dir d if not existed
  """
  try:
    os.makedirs(d)
    return d
  except OSError as e:
    if e.errno != errno.EEXIST:  # if the error is not 'already existed'
      raise
    else:
      return d


def lu2018_read_file_to_rawpd(fname):
  # Read from txt, delimiter is any space (' ' or '\t'), no header
  rawpd = pd.read_csv(fname, sep='\s+', header=None)
  
  # Set column names
  rawpd.columns = ['lon', 'lat', 'year'] + \
      ['lail{:02d}'.format(i+1) for i in range(nmon)] + \
      ['laih{:02d}'.format(i+1) for i in range(nmon)] + \
      ['cvl{:02d}'.format(i+1) for i in range(nmon)] + \
      ['cvh{:02d}'.format(i+1) for i in range(nmon)] + \
      ['vtl', 'vth']
  
  return rawpd


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


def test_loop_output():
  for i in range(10407):
    print(i)


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
  # for i in range(100):
  #   print(i)

  # return
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
    if cook['vtl_dom'][i] != 0:  # dominated by no veg
      mask = cook['vtl'][:, i] == cook['vtl_dom'][i]
      cook['cvl_dom_avg'][:, i] = np.mean( cook['cvl'][mask, :, i], axis=0)
  
    # Find the year indices of the dominant high veg type
    if cook['vth_dom'][i] != 0:  # dominated by no veg
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
  
  
def lu2018_add_coordination_to_cook(cook):
  # lon and lat for each grid
  
  # Land RG grid
  lon_land = cook['lon']
  lat_land = cook['lat']
  
  # Global RG grid, west --> east, south --> north
  lon_rg, lat_rg = generate_global_reduced_gaussian_grid(nlon_N80, lat_N80)

  cook['lon_rg'] = lon_rg
  cook['lat_rg'] = lat_rg
  
  # Global regular 1x1 grid, west --> east, south --> north
  lon_11 = np.linspace(-179.5, 179.5, 360)
  lat_11 = np.linspace(-89.5, 89.5, 180)
  
  nlon_11 = lon_11.size
  nlat_11 = lat_11.size
  
  cook['lon_11'] = lon_11
  cook['lat_11'] = lat_11
  
  # Global regular lon with reduced Gaussian lat, west --> east, south --> north
  lon_gg = np.copy(lon_11)
  lat_gg = np.copy(lat_rg)
  
  nlon_gg = lon_gg.size
  nlat_gg = lat_gg.size
  
  cook['lon_gg'] = lon_gg
  cook['lat_gg'] = lat_gg

  # Land ind in global grid for RG grid
  land_ind = get_land_ind_in_glob_reduced_gaussian_grid(lon_land, lat_land, lon_rg, lat_rg)

  cook['land_ind'] = land_ind

#==============================================================================#
#
# Classes
#
#==============================================================================#

class DatasetLu2018():
  """
  " Dataset for the data used in Lu2018
  " All the dataset share the same coordinate system
  """
  # 10-year data
  nyear = 10
  
  # Number of grids on the land
  ngrid = None
  
  # lon and lat for reduced Gaussian grids on the land, 10407 points
  lon_land, lat_land = None, None
  
  # lon and lat for global reduced Gaussian grids
  lon_rg, lat_rg = None, None
  
  # lon and lat for global Gaussian grids
  lon_gg, lat_gg = None, None
  
  # lon and lat for global regular 1x1 grid
  lon_11, lat_11 = None, None
  
  # The index of lon and lat of land on a global reduced Gaussian grid
  land_ind = None
  
  # Set coordination
  coord_is_set = False
  
  
  @staticmethod
  def set_coordination(lon_land, lat_land):
    # number of grids on the land
    DatasetLu2018.ngrid = lon_land.size
  
    # Lon_land and lat_land keep the same for each year
    DatasetLu2018.lon_land = lon_land
    DatasetLu2018.lat_land = lat_land
  
    # Global reduced Gaussian grid, west --> east, south --> north
    DatasetLu2018.lon_rg, DatasetLu2018.lat_rg = generate_global_reduced_gaussian_grid(nlon_N80, lat_N80)
      
    # Global regular 1x1 grid, west --> east, south --> north
    DatasetLu2018.lon_11 = np.linspace(-179.5, 179.5, 360)
    DatasetLu2018.lat_11 = np.linspace(-89.5, 89.5, 180)
      
    # Global Gaussian grid with 360 regular lon, west --> east, south --> north
    DatasetLu2018.lon_gg = np.copy(DatasetLu2018.lon_11)
    DatasetLu2018.lat_gg = np.copy(DatasetLu2018.lat_rg)
    
    # Land ind in global grid for RG grid
    DatasetLu2018.land_ind = get_land_ind_in_glob_reduced_gaussian_grid( \
      lon_land, lat_land, DatasetLu2018.lon_rg, DatasetLu2018.lat_rg)
    
    # Coordination is set
    DatasetLu2018.coord_is_set = True

    
  def __init__(self, fname):
    """
    Raw data structure:
    x: lon | lat | year | lail01-laih12 | laih01-laih12 | cvl01-cvl12 | cvh01-cvh12 | vtl | vth
    y: all the land grid, loop for each year
    """
    
    # Use short names
    nyear = DatasetLu2018.nyear

    # Raw data
    raw = np.loadtxt(fname)
    nrow, ncol = raw.shape
    ngrid = int(nrow/nyear)
    
    # Set coordination
    lon_raw = np.reshape(raw[:, 0], (nyear, ngrid))
    lat_raw = np.reshape(raw[:, 1], (nyear, ngrid))
    if not DatasetLu2018.coord_is_set:
      DatasetLu2018.set_coordination(lon_raw[0,:], lat_raw[0,:])
  
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
    self.lail = np.transpose( np.reshape(raw[:,  3:15], (nyear, ngrid, nmon)), (0, 2, 1) )  # [year, mon, grid]
    self.laih = np.transpose( np.reshape(raw[:, 15:27], (nyear, ngrid, nmon)), (0, 2, 1) )  # [year, mon, grid]
    
    #
    # monthly mean coverage of low and high veg
    # The structure is similar with LAI
    #
    self.cvl = np.transpose( np.reshape(raw[:, 27:39], (nyear, ngrid, nmon)), (0, 2, 1) )  # [year, mon, grid]
    self.cvh = np.transpose( np.reshape(raw[:, 39:51], (nyear, ngrid, nmon)), (0, 2, 1) )  # [year, mon, grid]
    
    #
    # veg types, one type per year but may change interannually
    # ngrid
    # o o o ... o
    # ...         10 years
    # o o o ... o
    #
    self.vtl = np.reshape(raw[:, 51], (nyear, ngrid))
    self.vth = np.reshape(raw[:, 52], (nyear, ngrid))
  
    #
    # Processed data
    #
  
    ##### Find the the most frequent veg type during 10 years
    ##### So finally, for each grid, there is only one dominant type within 10 years
    self.vtl_dom = DatasetLu2018.get_dominant_vegetation_type(self.vtl)
    self.vth_dom = DatasetLu2018.get_dominant_vegetation_type(self.vth)
  
    ##### Calculate the 10 year monthly averaged vegetation coverage for each grid at each month
    # The dominant vegetation type is used.
    # ngrid
    # o o o ... o
    # ...          12 months
    # o o o ... o
    ##### 
    self.cvl_dom_avg = np.zeros((nmon, ngrid))
    self.cvh_dom_avg = np.zeros((nmon, ngrid))
  
    for i in range(ngrid):
      # Find the year indices of the dominant low veg type
      mask = self.vtl[:, i] == self.vtl_dom[i]
      self.cvl_dom_avg[:, i] = np.mean( self.cvl[mask, :, i], axis=0)
  
      # Find the year indices of the dominant high veg type
      mask = self.vth[:, i] == self.vth_dom[i]
      self.cvh_dom_avg[:, i] = np.mean( self.cvh[mask, :, i], axis=0)
  
    # Find the set of low veg types
    vtl_set = np.unique(self.vtl)  # low vegetation
    vtl_set = np.delete( vtl_set, np.argwhere(vtl_set == 0) )  # delete zero elements which does not make sense
  
    # Find the set of high veg types
    vth_set = np.unique(self.vth)
    vth_set = np.delete( vth_set, np.argwhere(vth_set == 0) )
  
    # Find the set of veg types
    vt_set = np.unique( np.concatenate((vtl_set, vth_set)) )  # all the vegetation types
  
    self.vtl_set = vtl_set
    self.vth_set = vth_set
    self.vt_set  = vt_set
  
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
  
    # cv_dom for each vegetation type
    self.cv_dom = np.zeros((nvt, nmon, ngrid))
    for v in vtl_set:
      mask = self.vtl_dom == v
      self.cv_dom[int(v-1)][:, mask] = self.cvl_dom_avg[:, mask]
  
    for v in vth_set:
      mask = self.vth_dom == v
      self.cv_dom[int(v-1)][:, mask] = self.cvh_dom_avg[:, mask]
  
    # Get tv_dom, either 0 or 100, each grid should have only one value for each year.
    self.tv_dom = np.zeros((nvt, ngrid))
    for v in vtl_set:
      mask = self.vtl_dom[:] == v
      self.tv_dom[int(v-1), mask] = 100.0  # in LPJG, only one vegetation can exist for low type
  
    for v in vth_set:
      mask = self.vth_dom[:] == v
      self.tv_dom[int(v-1), mask] = 100.0  # in LPJG, only one vegetation can exist for high type
    
    
  @staticmethod
  def get_dominant_vegetation_type(vt):
    """
    input:
    vt: [nyear, ngrid], vegetation type
    
    return:
    vt_dom: [ngrid], dominant vegetation type during the 10 years
    """
    
    # Use short names
    nyear = DatasetLu2018.nyear
    
    if DatasetLu2018.ngrid is None:
      print('Warning: Initiate an instance first to set ngrid.')
      return None
    else:
      ngrid = DatasetLu2018.ngrid
    
    # Set the initial data, each grid only has one dominant vegetation type during 10 years
    vt_dom = np.zeros((ngrid,))
  
    # Set the type bins to trap the numbers from 0 (no veg) to 20
    bins = np.arange(-0.5, 21, 1)
  
    # Loop for each grid
    for i in range(ngrid):
      # Find the distribution of low types during 10 years
      hist_l, _bins = np.histogram(vt[:, i], bins)
  
      # Find all the dominant types
      dominant_l_all = np.argwhere( hist_l == np.amax(hist_l) ).flatten()  # the indices of most frequent veg
  
      # If the dominant types are more than one, the last occurred one is considered dominant
      if dominant_l_all.size > 1:
        ilast = []
        for d in dominant_l_all:
          ilast.append( np.argwhere(vt[::-1, i] == d).flatten()[0] )  # the last occurence
        i1 = np.argmin(ilast)  # who occurs the last, notice the array is reversed
        vt_dom[i] = dominant_l_all[i1]
      # Just use the value if only one dominant type
      else:
        vt_dom[i] = dominant_l_all[0]
      
    return vt_dom
  
  
  def get_data_on_regular_grid(self):
    # Use short names
    lon_gg, lat_gg = DatasetLu2018.lon_gg, DatasetLu2018.lat_gg
    nlon_gg, nlat_gg = lon_gg.size, lat_gg.size
    
    lon_11, lat_11 = DatasetLu2018.lon_11, DatasetLu2018.lat_11
    nlon_11, nlat_11 = lon_11.size, lat_11.size
    
    # Initialize the data array
    self.tv_dom_gg      = np.zeros( (nvt , nlat_gg, nlon_gg) )
    self.tv_dom_11      = np.zeros( (nvt , nlat_11, nlon_11) )
    self.cvh_dom_avg_gg = np.zeros( (nmon, nlat_gg, nlon_gg) )
    self.cvh_dom_avg_11 = np.zeros( (nmon, nlat_11, nlon_11) )
    self.cvl_dom_avg_gg = np.zeros( (nmon, nlat_gg, nlon_gg) )
    self.cvl_dom_avg_11 = np.zeros( (nmon, nlat_11, nlon_11) )    

    # Interpolate tv for each veg type with nearest method
    print('Interpolating tv_dom ...')
    for iv in range(nvt):
      print('{0:d}'.format(int(iv+1)))
      self.tv_dom_gg[int(iv), :, :], self.tv_dom_11[int(iv), :, :] = \
        DatasetLu2018.interpolate_data_from_lrg_to_11(self.tv_dom[int(iv), :], kind='nearest')
    
    # Interpolate cvl_dom_avg and cvh_dom_avg for each month with linear method
    for im in range(nmon):
      print('{0:d}'.format(int(im+1)))
      self.cvl_dom_avg_gg[int(im), :, :], self.cvl_dom_avg_11[int(im), :, :] = \
        DatasetLu2018.interpolate_data_from_lrg_to_11(self.cvl_dom_avg[int(im), :], kind='linear')
      self.cvh_dom_avg_gg[int(im), :, :], self.cvh_dom_avg_11[int(im), :, :] = \
        DatasetLu2018.interpolate_data_from_lrg_to_11(self.cvh_dom_avg[int(im), :], kind='linear')
  
  
  @classmethod
  def interpolate_data_from_lrg_to_11(cls, data_land, kind='linear'):
    """
    " Interpolate the scattered data to regular lon-lat coordinates
    " 
    " Now the bi-linear interpolation is used to get the coverage for the grid cells:
    " 
    " Check if the sizes of land lon and lat are correct
    " Generate the global grid ll: lon_glob, lat_glob
    " Generate regular global grid for reduced Gaussian latitudes and 1 degree lat
    " Obtain the indices of lon and lat for each land grid in the global grid: land_ind
    " Interpolation:
    "   (1) Loop for each latitude
    "   (2) Put the land data to global grid for reduced Gaussian grid
    "   (3) Interpolate every latitude from global reduced Gaussian to global regular grid
    "   (4) Interpolate for every longitude in the regular grid
    "
    " lon_land: lon for land grid
    " lat_land: lat for land grid
    " data_land: data at land grid
    " lon_glob: lon of global reduced Gaussian (RG) grid for each lat
    " lat_glob: lat of global RG grid
    " nlon_rgn: number of lon at each RG grid lat at NH
    " lon_11: lon of regular grid
    " lat_11: lat of regular grid
    " kind: interpolation method used in scipy.interpolate
    """
    
    # Use short names
    lon_land, lat_land = cls.lon_land, cls.lat_land
    nlon_land, nlat_land = lon_land.size, lat_land.size
    
    lon_rg, lat_rg = cls.lon_rg, cls.lat_rg
    
    lon_11, lat_11 = cls.lon_11, cls.lat_11
    nlon_11, nlat_11 = lon_11.size, lat_11.size
    
    lon_gg, lat_gg = cls.lon_gg, cls.lat_gg
    nlon_gg, nlat_gg = lon_gg.size, lat_gg.size
    
    land_ind = cls.land_ind
    
    ngrid = cls.ngrid
    
    #
    # Interpolation from data_land to data_regrg, then to data_reg
    #
    
    # Initiation
    data_gg = np.zeros((nlat_gg, nlon_gg))
    data_11 = np.zeros((nlat_11, nlon_11))
    
    data_rg = []  # data at global RG grid
    for j in range(lat_rg.size):
      data_rg.append( np.zeros((lon_rg[j].size,)) )
  
    # If data_land is all zero, return
    if np.amax(data_land) <= 0:
      print('No data for this vegetation type.')
      return data_gg, data_11
    
    # Put land data to data_glob
    for ig in range(ngrid):
      ilon, ilat = land_ind[ig, :]
      data_rg[ilat][ilon] = data_land[ig]
    
    # Interpolate for each lat at RG grid
    for ilatgg in range(nlat_gg):
      ##### Old interpolation method
      # data_regrg[ilatrg, :] = np.interp(lon_regrg, lon_glob[ilatrg][:], data_glob[ilatrg][:], period=360)
  
      ##### New interpolation method
      # Construct data set representing the period data
      x = np.concatenate([ [lon_rg[ilatgg][-1]-360.0], lon_rg[ilatgg][:], [lon_rg[ilatgg][0]+360.0] ])
      y = np.concatenate([ [data_rg[ilatgg][-1]], data_rg[ilatgg][:], [data_rg[ilatgg][0]] ])
  
      # Interpolate with method kind
      f = interpolate.interp1d(x, y, kind=kind)
      data_gg[ilatgg, :] = f(lon_gg)
  
      # Interpolate for each lon_reg from RG lat to regular lat: gg --> 11
      # 0 for external points, and remember to keep xp increment
      for ilon in range(nlon_11):
        # Old interpolation method, can not select interpolation method
        # data_reg[:, ilon] = np.interp(lat_reg, lat_regrg[::-1], data_regrg[::-1, ilon], left=0, right=0)
  
        # New interpolation method, make sure x is in the increment order
        f = interpolate.interp1d(lat_gg, data_gg[:, ilon], kind=kind, fill_value=0.0, bounds_error=False)
        data_11[:, ilon] = f(lat_11)
    
    return data_gg, data_11
  

  def save_data(self, fname):
    # Save the data
    np.savez(fname, \
             lon_land = DatasetLu2018.lon_land, \
             lat_land = DatasetLu2018.lat_land, \
             lon_11 = DatasetLu2018.lon_11, \
             lat_11 = DatasetLu2018.lat_11, \
             vtl_set = self.vtl_set, \
             vth_set = self.vth_set, \
             vt_set = self.vt_set, \
             lail = self.lail, \
             laih = self.laih, \
             tv_dom = self.tv_dom, \
             cvh_dom_avg = self.cvh_dom_avg, \
             cvl_dom_avg = self.cvl_dom_avg, \
             tv_dom_11 = self.tv_dom_11, \
             cvh_dom_avg_11 = self.cvh_dom_avg_11, \
             cvl_dom_avg_11 = self.cvl_dom_avg_11 \
            )

  
class TestStaticVariable():
  sta1 = 2.0
  
  def __init__(self):
    # self.sta1 = 3.0
    print(self.sta1, TestStaticVariable.sta1)


def show_statistics(data):
  """
  Show main information of a dataset:
  min, 25% quantile, median, 75% quantile, max
  mean, std
  """
  _min    = np.nanmin(data)
  _max    = np.nanmax(data)
  _q1     = np.quantile(data, 0.25)
  _q3     = np.quantile(data, 0.75)
  _median = np.nanmedian(data)
  _mean   = np.nanmean(data)
  _std    = np.nanstd(data)
  
  print('{0:>12s}{1:>12s}{2:>12s}{3:>12s}{4:>12s}{5:>12s}{6:>12s}'.format('min', 'q1', 'median', 'q3', 'max', 'mean', 'std'))
  print('{0:12.3e}{1:12.3e}{2:12.3e}{3:12.3e}{4:12.3e}{5:12.3e}{6:12.3e}'.format(_min, _q1, _median, _q3, _max, _mean, _std))
  # print('{0:>12s}{1:>12s}'.format('mean', 'std'))
  # print('{0:12.3e}{1:12.3e}'.format(_mean, _std))
  
  return (_min, _q1, _median, _q3, _max, _mean, _std)


def read_Lu2018_lpjg_data(fname):
  """
  Data structure:
    Variables: in each text file, x axis: lon, lat, year,
               12-month LAI of low veg, 12-month LAI of high veg,
               12-month coverage of low veg, 12-month coverage of high veg,
               low veg type, high veg type
  """
  nyear = 10  # 10-year data
  nmon  = 12  # 12 months
  
  # Raw data
  raw = np.loadtxt(fname)
  nrow, ncol = raw.shape
  ngrid = int(nrow/nyear)

  
  #
  # Organized data
  #

  data = {}

  # number of year
  data['nyear'] = 10

  # number of grids on the land
  data['ngrid'] = ngrid

  # longitude and latitude
  lon_raw = np.reshape(raw[:, 0], (nyear, ngrid))
  lat_raw = np.reshape(raw[:, 1], (nyear, ngrid))

  # Lon and lat keep the same for each year
  data['lon'] = lon_raw[0,:]
  data['lat'] = lat_raw[0,:]

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
  data['lail'] = np.transpose( np.reshape(raw[:,  3:15], (nyear, ngrid, nmon)), (0, 2, 1) )  # [year, mon, grid]
  data['laih'] = np.transpose( np.reshape(raw[:, 15:27], (nyear, ngrid, nmon)), (0, 2, 1) )  # [year, mon, grid]
  
  #
  # monthly mean coverage of low and high veg
  # The structure is similar with LAI
  #
  data['cvl'] = np.transpose( np.reshape(raw[:, 27:39], (nyear, ngrid, nmon)), (0, 2, 1) )  # [year, mon, grid]
  data['cvh'] = np.transpose( np.reshape(raw[:, 39:51], (nyear, ngrid, nmon)), (0, 2, 1) )  # [year, mon, grid]
  
  #
  # veg types, one type per year but may change interannually
  # ngrid
  # o o o ... o
  # ...         10 years
  # o o o ... o
  #
  data['vtl'] = np.reshape(raw[:, 51], (nyear, ngrid))
  data['vth'] = np.reshape(raw[:, 52], (nyear, ngrid))

  #
  # Processed data
  #

  ##### Find the the most frequent veg type during 10 years
  ##### So finally, for each grid, there is only one dominant type within 10 years

  # Set the initial data, each grid only has one dominant vegetation type during 10 years
  data['vtl_dom'] = np.zeros((ngrid,))
  data['vth_dom'] = np.zeros((ngrid,))

  # Set the type bins to trap the numbers from 0 to 20
  bins = np.arange(-0.5, 21, 1)

  # Loop for each grid
  for i in range(ngrid):
    # Find the distribution of low types during 10 years
    hist_l, _bins = np.histogram(data['vtl'][:, i], bins)

    # Find all the dominant types
    dominant_l_all = np.argwhere( hist_l == np.amax(hist_l) ).flatten()  # the indices of most frequent veg

    # If the dominant types are more than one, the last occurred one is considered dominant
    if dominant_l_all.size > 1:
      ilast = []
      for d in dominant_l_all:
        ilast.append( np.argwhere(data['vtl'][::-1, i] == d).flatten()[0] )  # the last occurence
      i1 = np.argmin(ilast)  # who occurs the last, notice the array is reversed
      data['vtl_dom'][i] = dominant_l_all[i1]
    # Just use the value if only one dominant type
    else:
      data['vtl_dom'][i] = dominant_l_all[0]

    # Do the same for high veg

    # Find the distribution of high types during 10 years
    hist_h, _bins = np.histogram(data['vth'][:, i], bins)

    # Find all the dominant types
    dominant_h_all = np.argwhere( hist_h == np.amax(hist_h) ).flatten()  # the indices of most frequent veg

    # If the dominant types are more than one, the last occurred one is considered dominant
    if dominant_h_all.size > 1:
      ilast = []
      for d in dominant_h_all:
        ilast.append( np.argwhere(data['vth'][::-1, i] == d).flatten()[0] )  # the last occurence
      i1 = np.argmin(ilast)  # who occurs the last, notice the array is reversed
      data['vth_dom'][i] = dominant_h_all[i1]
    # Just use the value if only one dominant type
    else:
      data['vth_dom'][i] = dominant_h_all[0]

  ##### Calculate the 10 year monthly averaged vegetation coverage for each grid at each month
  # The dominant vegetation type is used.
  # ngrid
  # o o o ... o
  # ...          12 months
  # o o o ... o
  ##### 
  data['cvl_dom_avg'] = np.zeros((nmon, ngrid))
  data['cvh_dom_avg'] = np.zeros((nmon, ngrid))

  for i in range(ngrid):
    # Find the year indices of the dominant low veg type
    mask = data['vtl'][:, i] == data['vtl_dom'][i]
    data['cvl_dom_avg'][:, i] = np.mean( data['cvl'][mask, :, i], axis=0)

    # Find the year indices of the dominant high veg type
    mask = data['vth'][:, i] == data['vth_dom'][i]
    data['cvh_dom_avg'][:, i] = np.mean( data['cvh'][mask, :, i], axis=0)

  # 10-year averaged LAI, [ngrid]
  # data['lail_10a_avg'] = np.mean(data['lail'], axis=(0, 1))
  # data['laih_10a_avg'] = np.mean(data['laih'], axis=(0, 1))

  # 10-year averaged coverage, [ngrid]
  # data['cvl_10a_avg'] = np.mean(data['cvl'], axis=(0, 1))
  # data['cvh_10a_avg'] = np.mean(data['cvh'], axis=(0, 1))

  # 10-year veg type, [ngrid]
  data['vtl_10a_avg'] = np.mean(data['vtl'], axis=0)
  data['vth_10a_avg'] = np.mean(data['vth'], axis=0)

  ##### Monthly mean coverage for different veg types
  
  # Find the set of low veg types
  vtl_set = np.unique(data['vtl'])  # low vegetation
  vtl_set = np.delete( vtl_set, np.argwhere(vtl_set == 0) )  # delete zero elements which does not make sense

  # Find the set of high veg types
  vth_set = np.unique(data['vth'])
  vth_set = np.delete( vth_set, np.argwhere(vth_set == 0) )

  # Find the set of veg types
  vt_set = np.unique( np.concatenate((vtl_set, vth_set)) )  # all the vegetation types

  data['vtl_set'] = vtl_set
  data['vth_set'] = vth_set
  data['vt_set']  = vt_set

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

  # cv, usually is not needed
  # data['cv'] = np.zeros((nvt, nyear, nmon, ngrid))
  # for iy in range(nyear):
  #   for v in vtl_set:
  #     mask = data['vtl'][iy, :] == v
  #     data['cv'][int(v-1), iy, :, mask] = data['cvl'][iy, :, mask]

  #   for v in vth_set:
  #     mask = data['vth'][iy, :] == v
  #     data['cv'][int(v-1), iy, :, mask] = data['cvh'][iy, :, mask]

  # cv_dom
  data['cv_dom'] = np.zeros((nvt, nmon, ngrid))
  for v in vtl_set:
    mask = data['vtl_dom'] == v
    data['cv_dom'][int(v-1)][:, mask] = data['cvl_dom_avg'][:, mask]

  for v in vth_set:
    mask = data['vth_dom'] == v
    data['cv_dom'][int(v-1)][:, mask] = data['cvh_dom_avg'][:, mask]

  # Get tv_dom, either 0 or 100, each grid should have only one value for each year.
  data['tv_dom'] = np.zeros((nvt, ngrid))
  for v in vtl_set:
    mask = data['vtl_dom'][:] == v
    # Use a mixing of basic and advanced indexing to prevent shape error
    data['tv_dom'][int(v-1), mask] = 100.0  # in LPJG, only one vegetation can exist for low type

  for v in vth_set:
    mask = data['vth_dom'][:] == v
    # Use a mixing of basic and advanced indexing to prevent shape error
    data['tv_dom'][int(v-1), mask] = 100.0  # in LPJG, only one vegetation can exist for high type
  
  return data


def write_veg_change_history(data, fout):
  """
  At some grid cells the vegetation type will change with time during 10 years.
  So here we record the altering history of these grids, including:
  grid number, grid id, lon, lat, vegetation type for 10 years

  data: input lu2018 data pack
  fout: output file name
  """

  with open(fout, 'w') as f:
    # Header
    f.write( ('{:>6s}{:>6s}{:>8s}{:>8s}{:^30s}{:>5s}\n').format('no', 'id|0-', 'lon', 'lat', 'low veg type', 'doml') )

    # Changing history of low vegetation
    for i, ig in enumerate( np.argwhere( data['vtl'][0, :] != data['vtl_10a_avg'] ) ):  # the veg type has changed within 10 years
      ind = ig[0]
      fstr = '{:6d}{:6d}{:8.2f}{:8.2f}' + 10*'{:3.0f}' + '{:5.0f}' + '\n'
      f.write( fstr.format(i, ind, data['lon'][ind], data['lat'][ind], *data['vtl'][:, ind], data['vtl_dom'][ind]) )

    # Header
    f.write( ('{:>6s}{:>6s}{:>8s}{:>8s}{:^30s}{:>5s}\n').format('no', 'id|0-', 'lon', 'lat', 'high veg type', 'domh') )

    # Changing history of high vegetation
    for i, ig in enumerate( np.argwhere( data['vth'][0, :] != data['vth_10a_avg'] ) ):  # the veg type has changed within 10 years
      ind = ig[0]
      fstr = '{:6d}{:6d}{:8.2f}{:8.2f}' + 10*'{:3.0f}' + '{:5.0f}' + '\n'
      f.write( fstr.format(i, ind, data['lon'][ind], data['lat'][ind], *data['vth'][:, ind], data['vth_dom'][ind]) )

  return


def generate_global_reduced_gaussian_grid(nlon_rgn, lat_rgn):
  """
  " Generate the global reduced Gaussian grid from nlon and lat of reduced Gaussian grid
  """
  
  ##### Global lat from south to north
  nlat_glob = 2*lat_rgn.size
  lat_glob = np.zeros((nlat_glob,))

  # NH
  lat_glob[0:int(nlat_glob/2)] = lat_rgn

  # SH
  lat_glob[int(nlat_glob/2):] = - lat_rgn[::-1]

  # Reverse to sort from south to north
  lat_glob = lat_glob[::-1]
  
  ##### Global lon from west to east, 0 is about in the middle
  ##### lon: a list of arrays
  # Combine the NH and SH
  nlon_glob = np.concatenate( [nlon_rgn, nlon_rgn[::-1]] )

  # Initiate
  lon_glob = []

  # Loop for each lat
  for i, n in enumerate(nlon_glob):
    dl = 360.0/n  # lon interval for each lat
    if n % 2 == 1:  # n is odd
      l0 = -180.0 + dl/2.0
      l1 = 180.0 - dl/2.0
      n0 = int((n-1)/2)
    else:  # n is even
      l0 = -180.0 + dl
      l1 = 180.0
      n0 = int((n-2)/2)
    n1 = n - n0
  
    # 0 degree must be included in the reduced Gaussian grid
    lon_temp = np.concatenate([np.linspace(l0, 0, n0, endpoint=False), np.linspace(0, l1, n1)])

    # Add the lon array to the lon_glob list
    lon_glob.append(lon_temp)

  return lon_glob, lat_glob


def get_land_ind_in_glob_reduced_gaussian_grid(lon_land, lat_land, lon_glob, lat_glob):
  """
  " Obtain the indices of lon and lat for each land grid in the global grid: land_ind
  "
  " Find lon and lat indices for land grids in global grids
  " For the i-th grid saved in the Lu2018 data,
  " the land lon and lat are: lon_land[i], lat_land[i]
  " the lon and lat in the global grid: lon_glob[land_ind[i, 1]][land_ind[i, 0]], lat_glob[land_ind[i, 1]]
  " In order to verify if the point in land and globe is close enough,
  " differences of lon and lat are calculated as diff_lg for each point at land grid and global grid.
  """
  ngrid_land = lon_land.size

  land_ind = np.zeros((ngrid_land, 2)).astype(int)  # save the lon and lat index in the global grid
  for i, (lon, lat) in enumerate(zip(lon_land, lat_land)):
    # lat
    ilat = (np.abs(lat - lat_glob)).argmin()
  
    # lon
    ilon = (np.abs(lon - lon_glob[ilat])).argmin()
  
    # Save the indices to the land_ind array
    land_ind[i, :] = ilon, ilat
    
  return land_ind


def interp_land_reduced_gaussian_regular_grid(lon_land, lat_land, land_ind, data_land, \
  lon_glob, lat_glob, lon_regrg, lat_regrg, lon_reg, lat_reg, kind='linear'):
  """
  " Interpolate the scattered data to regular lon-lat coordinates
  " 
  " Now the bi-linear interpolation is used to get the coverage for the grid cells:
  " 
  " Check if the sizes of land lon and lat are correct
  " Generate the global grid ll: lon_glob, lat_glob
  " Generate regular global grid for reduced Gaussian latitudes and 1 degree lat
  " Obtain the indices of lon and lat for each land grid in the global grid: land_ind
  " Interpolation:
  "   (1) Loop for each latitude
  "   (2) Put the land data to global grid for reduced Gaussian grid
  "   (3) Interpolate every latitude from global reduced Gaussian to global regular grid
  "   (4) Interpolate for every longitude in the regular grid
  "
  " lon_land: lon for land grid
  " lat_land: lat for land grid
  " data_land: data at land grid
  " lon_glob: lon of global reduced Gaussian (RG) grid for each lat
  " lat_glob: lat of global RG grid
  " nlon_rgn: number of lon at each RG grid lat at NH
  " lon_reg: lon of regular grid
  " lat_reg: lat of regular grid
  " kind: interpolation method used in scipy.interpolate
  """

  #
  # Check if the sizes of land lon and lat are correct
  #
  nlon_land = lon_land.size
  nlat_land = lat_land.size
  if nlon_land != nlat_land:
    print('Error: numbers of lon and lat on the land are not equal.')
    return
  else:
    ngrid_land = nlon_land
  
  # regular global grid, e.g., 1x1
  nlon_reg = lon_reg.size
  nlat_reg = lat_reg.size
  
  # regular lon with reduced Gaussian lat
  nlon_regrg = lon_regrg.size
  nlat_regrg = lat_regrg.size
  
  #
  # Interpolation from data_land to data_regrg, then to data_reg
  #
  
  # Initiation
  data_regrg = np.zeros((nlat_regrg, nlon_regrg))
  data_reg   = np.zeros((nlat_reg, nlon_reg))
  
  data_glob = []  # data at global RG grid
  for j in range(lat_glob.size):
    data_glob.append( np.zeros((lon_glob[j].size,)) )

  # If data_land is all zero, return
  if np.max(data_land) <= 0:
    print('No data for this vegetation type.')
    return data_regrg, data_reg
  
  # Put land data to data_glob
  for ig in range(ngrid_land):
    ilon, ilat = land_ind[ig, :]
    data_glob[ilat][ilon] = data_land[ig]
  
  # Interpolate for each lat at RG grid
  for ilatrg in range(nlat_regrg):
    # Old interpolation method
    # data_regrg[ilatrg, :] = np.interp(lon_regrg, lon_glob[ilatrg][:], data_glob[ilatrg][:], period=360)

    ##### New interpolation method
    # Construct data set representing the period data
    # print(ilatrg, lon_glob[ilatrg])
    x = np.concatenate([ [lon_glob[ilatrg][-1]-360.0], lon_glob[ilatrg][:], [lon_glob[ilatrg][0]+360.0] ])
    y = np.concatenate([ [data_glob[ilatrg][-1]], data_glob[ilatrg][:], [data_glob[ilatrg][0]] ])

    # Interpolate with method kind
    f = interpolate.interp1d(x, y, kind=kind)
    data_regrg[ilatrg, :] = f(lon_regrg)

    # Interpolate for each lon_reg from RG lat to regular lat: regrg --> reg
    # 0 for external points, and remember to keep xp increment
    for ilon in range(nlon_reg):
      # Old interpolation method, can not select interpolation method
      # data_reg[:, ilon] = np.interp(lat_reg, lat_regrg[::-1], data_regrg[::-1, ilon], left=0, right=0)

      # New interpolation method, make sure x is in the increment order
      f = interpolate.interp1d(lat_regrg[::-1], data_regrg[::-1, ilon], kind=kind, fill_value=0.0, bounds_error=False)
      data_reg[:, ilon] = f(lat_reg)
  
  return data_regrg, data_reg


def create_tm5_input_veg_file(fname, lon, lat, tv, cvh, cvl, fid_raw, verb=False, output='output_veg.txt'):
# def create_tm5_input_veg_file(fname, lon, lat, tv, cvh, cvl, fid_raw):
  """
  " fname: name of tm5 input veg hdf4 file
  " input_data: including tv, cvh, cvl, lon, lat
  " fid_raw: 
  """

  # Delete file if exists, so create a totally new file
  if os.path.exists(fname):
    os.remove(fname)
  
  # Read input data modified from Lu2018
  # tv  = input_data['tv_dom_11']
  # cvh = input_data['cvh_dom_avg_11']
  # cvl = input_data['cvl_dom_avg_11']
  # lon = input_data['lon_11']
  # lat = input_data['lat_11']
  nlon, nlat = lon.size, lat.size
  
  # Open a file to write
  fid = SD(fname, SDC.WRITE|SDC.CREATE)
  
  # Set global attributes according to fid_raw
  fid.ae       = fid_raw.ae
  fid.area_m2  = fid_raw.area_m2
  fid.fname    = fname
  fid.format   = fid_raw.format
  fid.grav     = fid_raw.grav
  fid.gridtype = fid_raw.gridtype
  fid.latmax   = fid_raw.latmax
  fid.latmin   = fid_raw.latmin
  fid.lonmax   = fid_raw.lonmax
  fid.lonmin   = fid_raw.lonmin
  
  # Create datasets for lon and lat
  d = fid.create('LAT', SDC.FLOAT64, nlat)
  dim0 = d.dim(0)
  dim0.setname('LAT')
  d[:] = lat
  d.endaccess()
  
  d = fid.create('LON', SDC.FLOAT64, nlon)
  dim0 = d.dim(0)
  dim0.setname('LON')
  d[:] = lon
  d.endaccess()
  
  # Create datasets for tv
  for i in range(nvt):
    tvstr = tm5_tvname[i]
    d = fid.create(tvstr, SDC.FLOAT64, (nlat, nlon))
    dim0 = d.dim(0)
    dim1 = d.dim(1)
    dim0.setname('LAT')
    dim1.setname('LON')
  
    d[:] = tv[i, :, :]
  
    # Close dataset
    d.endaccess()
  
  # Create datasets for cvh and cvl
  d = fid.create('cvh', SDC.FLOAT64, (nlat, nlon))
  dim0 = d.dim(0)
  dim1 = d.dim(1)
  dim0.setname('LAT')
  dim1.setname('LON')
  d[:] = cvh
  d.endaccess()
  
  d = fid.create('cvl', SDC.FLOAT64, (nlat, nlon))
  dim0 = d.dim(0)
  dim1 = d.dim(1)
  dim0.setname('LAT')
  dim1.setname('LON')
  d[:] = cvl
  d.endaccess()
  
  # Add variable attributes the same as in tm5 veg 2009 raw file
  ds_names = fid.datasets()
  ds_raw = fid_raw.select('tv01')
  for dn in ds_names:
    ds = fid.select(dn)
    if not ds.iscoordvar():
      for attr_name, attr_value in ds_raw.attributes().items():
        setattr(ds, attr_name, attr_value)
  
  # Close file
  fid.end()
  # fid_raw.end()
  
  # Check file info
  fid, fattr, fdset = pf.h4dump(fname, verb, output)

  return fid, fattr, fdset


def modify_potsrc(region):
  """
  " region: (W, E, S, N)
  """
  pass


def modify_soilph(lon, lat, soilph, cvh, cvl, region):
  """
  " Modify soilph3 and soilph4 according to cvh and cvl in the region
  "
  " In emission_dust.F90: the area with soilph(3) + soilph(4) > 0 is considered as desert
  " Lu2018: bare soil is set where vegetation cover < 20%.
  " So here we set both the soilph(3) and soilph(4) to 0 (not desert) when cvh + cvl >= 0.2 in the northern African region (e.g., 20W-40E, 10N-30N).
  " Notice the index of 3 and 4 are 2 and 3.
  "
  " lon, lat: coordinates
  " soilph: [nsoilph, nlat, nlon], nsoilph = 5
  " cvh, cvl: [nlat, nlon]
  " region: (W, E, S, N)
  "
  " Here cvh, cvl and soilph should be in the same global grid, e.g., 1x1
  """

  # Region mask
  regm_lon = (lon>=region[0]) & (lon<=region[1])
  regm_lat = (lat>=region[2]) & (lat<=region[3])

  # Get cvh and cvl in the region
  cvh_reg = cvh[np.ix_(regm_lat, regm_lon)]
  cvl_reg = cvl[np.ix_(regm_lat, regm_lon)]
  
  # Extract the region, set regional soilph wrt cvh and cvl, then set back the values
  sp3_reg = np.squeeze( soilph[np.ix_([2], regm_lat, regm_lon)] )
  sp3_reg[cvh_reg+cvl_reg >= 0.2] = 0.0
  soilph[np.ix_([2], regm_lat, regm_lon)] = sp3_reg
  
  sp4_reg = np.squeeze( soilph[np.ix_([3], regm_lat, regm_lon)] )
  sp4_reg[cvh_reg+cvl_reg >= 0.2] = 0.0
  soilph[np.ix_([3], regm_lat, regm_lon)] = sp4_reg

  return soilph


def modify_onlinedust_4(fname_raw, region):
  pass


#==============================================================================#
#
# Plot functions
#
#==============================================================================#
def ll_to_xy_for_map_pcolor(lon, lat, pm, reg):
  m = create_basemap(pm, reg)

  # Calculate x, y from lon and lat only once, and extend lon and lat to the corners for pcolor
  dlon = lon[1] - lon[0]
  dlat = lat[1] - lat[0]
  lonp = np.concatenate( (lon-dlon*0.5, [lon[-1]+dlon*0.5]) )
  latp = np.concatenate( (lat-dlat*0.5, [lat[-1]+dlat*0.5]) )
  
  # Generate 2D mesh grid
  xp, yp = np.meshgrid(lonp, latp)
  xpm, ypm = m(xp, yp)

  return xpm, ypm


def create_basemap(pm, reg):
  m = Basemap(projection=pm, lon_0=0, llcrnrlat=reg[0], urcrnrlat=reg[1], llcrnrlon=reg[2], urcrnrlon=reg[3], resolution='l')
  return m


def plot_map(ax, pm, reg, parallels=np.arange(-90, 91, 15.0), meridians=np.arange(-180.0, 181.0, 30.0)):
  """
  " llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
  " are the lat/lon values of the lower left and upper right corners of the map.
  " resolution = 'c' means use crude resolution coastlines.
  """

  color = 'lightgray'

  # Create basemap
  # m = Basemap(projection='cyl', llcrnrlat=-50, urcrnrlat=-10, llcrnrlon=110, urcrnrlon=160, resolution='c', ax=ax)
  # m = Basemap(projection='cyl', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='l', ax=ax)
  # m = Basemap(projection='moll', lon_0=0, llcrnrlat=reg[0], urcrnrlat=reg[1], llcrnrlon=reg[2], urcrnrlon=reg[3], resolution='l', ax=ax)
  m = Basemap(projection=pm, lon_0=0, llcrnrlat=reg[0], urcrnrlat=reg[1], llcrnrlon=reg[2], urcrnrlon=reg[3], resolution='l', ax=ax)

  # Draw coastlines and fill the continent
  # If you do not want to show boundaries of inland lakes and rivers:
  # one way is: do not draw coast lines, set the same color for continent, lakes and rivers
  # the other way: also set the color of coast lines the same as others
  # m.drawcoastlines(linewidth=0.25)
  m.fillcontinents(color=color, lake_color=color)
  m.drawrivers(color=color)

  # Draw country boundaries
  # m.drawcountries(linewidth=0.25)

  # Draw parallels and meridians.
  # labels = [left,right,top,bottom]
  m.drawparallels(parallels, labels=[True, False, False, False], fontsize=18)  # draw latitude lines every 30 degrees
  m.drawmeridians(meridians, labels=[False, False, False, True], fontsize=18)  # draw longitude lines every 60 degrees
  # m.drawmapboundary(fill_color='aqua')  # draw the edge of map projection region

  # land-sea mask
  # m.drawlsmask(land_color='coral', ocean_color='aqua', lakes=False)
  
  return m


def plot_tv_dom(data, file_prefix):
  """
  " 
  " Plot veg coverage of dominant types if they exist
  " 
  " data: tv_dom[nvt, nmon, ngrid], the value is either 0 or 100
  " 
  " figure structure: plot for each veg type and month
  " 
  " Save to figures: <file_prefix>_tv##_mon##.png
  " 
  " 
  """

  # Loop for each veg type existed in lpjg or Lu2018 dataset
  for v in data['vt_set']:
    # Array index of veg type
    ind = int(v-1)

    # Set string for tv##
    tvname = tm5_tvname[ind]
  
    # Name of veg type
    vtname = tm5_vtname[ind]
  
    # Print info on the screen
    print('Ploting {0} {1} ...'.format(tvname, vtname))
  
    # Skip if the max coverage is 0
    if np.max(data['tv_dom'][ind, :, :]) <= 0:
      print('No {0} cover.'.format(tvname))
      continue

    for im in range(nmon):
    # for im in range(2):
      # Show some info
      print('-- Month {0:2.0f}'.format(im+1))

      # Initiate figure
      fg, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=DPI)

      # Initiate map
      m = plot_map(ax, 'moll', reg_glob)
  
      # Convert lon lat to x y coordinates
      x, y = m(data['lon'][-1, :], data['lat'][-1, :])
  
      # Data of current month
      z = data['tv_dom'][ind, int(im), :]
      zm = ma.array(z, mask=z==0)  # Do not draw 0 coverage
  
      # Plot the scatter plot
      cmap = plt.get_cmap('Greens')
      # h = m.scatter(x[mask], y[mask], c=z[mask], s=0.1, cmap=cmap, zorder=3)
      h = m.scatter(x, y, c=zm, vmin=100, vmax=100, s=4, marker='o', cmap=cmap, zorder=3)
  
      # Set figure title
      fg.suptitle('{0:s} {1:s} month {2:2.0f}'.format(tvname, vtname, im+1))  # , y=1.08)
  
      # Save the figure
      fg.tight_layout()
      fg.savefig('{0:s}_{1:s}_mon{2:02.0f}.png'.format(file_prefix, tvname, im+1), dpi=DPI)

  return


def plot_cv_dom_avg_reg(data, file_prefix):
  """
  " 
  " Plot veg coverage of dominant types if they exist
  " 
  " data: cv_dom_avg_reg11[nvt, nmon, nlon_reg11, nlat_reg11], 1x1 degrees regular grid
  " 
  " figure structure: plot for each veg type and month
  " 
  " Save to figures: <file_prefix>_tv##_mon##.png
  " 
  """

  # Loop for each veg type existed in lpjg or Lu2018 dataset
  for v in data['vt_set']:
    # Set string for tv##
    tv_str = 'tv{:02.0f}'.format(v)
  
    # Name of veg type
    vt_name = tm5_veg_type[tv_str]
  
    # Print info on the screen
    print('Ploting {0} {1} ...'.format(tv_str, vt_name))
  
    # Array index of veg type
    ind = int(v-1)
  
    # Skip if the max coverage is 0
    if np.max(data['cv_dom_avg_reg11'][ind, :, :, :]) <= 0:
      print('No {0} cover.'.format(tv_str))
      continue

    for im in range(nmon):
    # for im in range(2):
      # Show some info
      print('-- Month {0:2.0f}'.format(im+1))

      # Initiate figure
      fg, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=DPI)

      # Initiate map
      m = plot_map(ax, 'moll', reg_glob)
  
      # Convert lon lat to x y coordinates
      dlon = data['lon_reg11'][1] - data['lon_reg11'][0]
      dlat = data['lat_reg11'][1] - data['lat_reg11'][0]
      lon = np.concatenate( (data['lon_reg11']-dlon, [data['lon_reg11'][-1]+dlon,]) )
      lat = np.concatenate( (data['lat_reg11']-dlat, [data['lat_reg11'][-1]+dlat,]) )
      # print(data['lon_reg11'].shape, data['lat_reg11'].shape)
      x, y = np.meshgrid(lon, lat)
      px, py = m(x, y)
  
      # Data of current month
      z = np.copy( data['cv_dom_avg_reg11'][ind, int(im), :, :] )
      # print(np.max(z, axis=0))
      # print(np.min(z, axis=0))
      # return

      # Do not draw 0 coverage
      # mask = z == 0
      # z[mask] = np.nan
      zm = ma.array(z, mask= z < 0.2)
      print(zm[90, :])
  
      # Plot the scatter plot
      cmap = plt.get_cmap('Greens')
      # h_ms = m.scatter(x[mask], y[mask], c=z[mask], s=0.1, cmap=cmap, zorder=3)
      # h_ms = m.scatter(x[mask], y[mask], c=z[mask], vmin=0, vmax=1, s=4, marker='o', cmap=cmap, zorder=3)
      # h_ms = m.pcolormesh(x, y, z, vmin=0, vmax=1, s=4, marker='o', cmap=cmap, zorder=3)
      # h_ms = m.pcolormesh(px, py, z, vmin=0, vmax=1, cmap=cmap, zorder=3)
      h_ms = m.pcolormesh(px, py, zm, vmin=0, vmax=1, zorder=3)
      m.colorbar(h_ms)
  
      # Set figure title
      fg.suptitle('{0:s} {1:s} month {2:2.0f}'.format(tv_str, vt_name, im+1))  # , y=1.08)
  
      # Save the figure
      fg.tight_layout()
      fg.savefig('{0:s}_{1:s}_mon{2:02.0f}.png'.format(file_prefix, tv_str, im+1), dpi=DPI)

      return

  return


def plot_simple_pcolor_map(lon, lat, data, pm, region, fname):
  # Initiate fg and ax
  fg, ax = plt.subplots(1, 1, figsize=(12, 8), dpi=DPI)

  # Initiate map
  m = plot_map(ax, pm, region)
  
  # Convert lon lat to x y coordinates
  xpm, ypm = ll_to_xy_for_map_pcolor(lon, lat, pm, region)

  # Plot pcolor
  # Here data can be masked array
  h = m.pcolormesh(xpm, ypm, data, zorder=3)
  m.colorbar(h)
  
  # Set figure title
  # fg.suptitle('{0:s} {1:s} month {2:2.0f}'.format(tv_str, vt_name, im+1))  # , y=1.08)
  
  # Save the figure
  fg.tight_layout()
  fg.savefig(fname, dpi=DPI)

  return



#==============================================================================#
#
# Plot ases instead of the whole figure
#
# This is more flexible.
#
#==============================================================================#
def plotax_tv_dom(ax, data, file_prefix):
  """
  " 
  " Plot veg coverage of dominant types if they exist
  " 
  " data: tv_dom[nvt, nmon, ngrid], the value is either 0 or 100
  " 
  " figure structure: plot for each veg type and month
  " 
  " Save to figures: <file_prefix>_tv##_mon##.png
  " 
  " 
  """

  # Loop for each veg type existed in lpjg or Lu2018 dataset
  for v in data['vt_set']:
    # Array index of veg type
    ind = int(v-1)

    # Set string for tv##
    tvname = tm5_tvname[ind]
  
    # Name of veg type
    vtname = tm5_vtname[ind]
  
    # Print info on the screen
    print('Ploting {0} {1} ...'.format(tvname, vtname))
  
    # Skip if the max coverage is 0
    if np.max(data['tv_dom'][ind, :, :]) <= 0:
      print('No {0} cover.'.format(tvname))
      continue

    for im in range(nmon):
      # Show some info
      print('-- Month {0:2.0f}'.format(im+1))

      # Initiate map
      m = plot_map(ax, 'moll', reg_glob)
  
      # Convert lon lat to x y coordinates
      x, y = m(data['lon'][-1, :], data['lat'][-1, :])
  
      # Data of current month
      z = data['tv_dom'][ind, int(im), :]
      zm = ma.array(z, mask=z==0)  # Do not draw 0 coverage
  
      # Plot the scatter plot
      cmap = plt.get_cmap('Greens')
      # h = m.scatter(x[mask], y[mask], c=z[mask], s=0.1, cmap=cmap, zorder=3)
      h = m.scatter(x, y, c=zm, vmin=100, vmax=100, s=4, marker='o', cmap=cmap, zorder=3)
  
  return m, h


def plotax_scatter(ax, lon, lat, datam, vmin=0, vmax=1, pm='cyl', reg=reg_glob, cmap = plt.get_cmap('Greens')):
  """
  " 
  " Plot scatter plot on map
  " lon, lat: ll coordinates
  " datam: masked data array
  " 
  """
  # Initiate map
  m = plot_map(ax, pm=pm, reg=reg)
  
  # Convert lon lat to x y coordinates
  x, y = m(lon, lat)
  
  # Plot the scatter plot
  h = m.scatter(x, y, c=datam, vmin=vmin, vmax=vmax, s=4, marker='o', cmap=cmap, zorder=3)
  
  return m, h


def plotax_pcolormesh(ax, lon, lat, datam, vmin=None, vmax=None, pm='cyl', reg=reg_glob, cmap = plt.get_cmap('Greens'), alpha=1.0):
  """
  " 
  " Plot pcolor plot on map
  " lon, lat: ll coordinates, they should be increment
  " datam: masked data array
  " 
  """
  # Initiate map
  m = plot_map(ax, pm=pm, reg=reg)
  
  # Convert lon lat to x y coordinates,
  # 1: extend the lon and lat, one more grid than data in both directions
  # 2: use meshgrid to generate the coordinates
  dlon = (lon[1] - lon[0])*0.5
  dlat = (lat[1] - lat[0])*0.5
  lon = np.concatenate( (lon-dlon, [lon[-1]+dlon,]) )
  lat = np.concatenate( (lat-dlat, [lat[-1]+dlat,]) )
  x, y = np.meshgrid(lon, lat)
  px, py = m(x, y)
  
  # Plot the pcolormesh plot
  if (vmin is not None) and (vmax is not None):
    h = m.pcolormesh(px, py, datam, vmin=vmin, vmax=vmax, cmap=cmap, zorder=3, alpha=alpha)
  else:
    h = m.pcolormesh(px, py, datam, cmap=cmap, zorder=3, alpha=alpha)
  
  return m, h



# Create tm5 input vegetation files in the netcdf format
def create_tm5_input_veg_file_netcdf(fname, lon, lat, tv, cvh, cvl, fid_raw, verb=False, output='output_veg.txt'):
# def create_tm5_input_veg_file(fname, lon, lat, tv, cvh, cvl, fid_raw):
  """
  " fname: name of tm5 input veg hdf4 file
  " input_data: including tv, cvh, cvl, lon, lat
  " fid_raw: 
  """

  # Delete file if exists, so create a totally new file
  if os.path.exists(fname):
    os.remove(fname)
  
  # Read input data modified from Lu2018
  # tv  = input_data['tv_dom_11']
  # cvh = input_data['cvh_dom_avg_11']
  # cvl = input_data['cvl_dom_avg_11']
  # lon = input_data['lon_11']
  # lat = input_data['lat_11']
  nlon, nlat = lon.size, lat.size
  
  # Open a file to write
  fid = SD(fname, SDC.WRITE|SDC.CREATE)
  
  # Set global attributes according to fid_raw
  fid.ae       = fid_raw.ae
  fid.area_m2  = fid_raw.area_m2
  fid.fname    = fname
  fid.format   = fid_raw.format
  fid.grav     = fid_raw.grav
  fid.gridtype = fid_raw.gridtype
  fid.latmax   = fid_raw.latmax
  fid.latmin   = fid_raw.latmin
  fid.lonmax   = fid_raw.lonmax
  fid.lonmin   = fid_raw.lonmin
  
  # Create datasets for lon and lat
  d = fid.create('LAT', SDC.FLOAT64, nlat)
  dim0 = d.dim(0)
  dim0.setname('LAT')
  d[:] = lat
  d.endaccess()
  
  d = fid.create('LON', SDC.FLOAT64, nlon)
  dim0 = d.dim(0)
  dim0.setname('LON')
  d[:] = lon
  d.endaccess()
  
  # Create datasets for tv
  for i in range(nvt):
    tvstr = tm5_tvname[i]
    d = fid.create(tvstr, SDC.FLOAT64, (nlat, nlon))
    dim0 = d.dim(0)
    dim1 = d.dim(1)
    dim0.setname('LAT')
    dim1.setname('LON')
  
    d[:] = tv[i, :, :]
  
    # Close dataset
    d.endaccess()
  
  # Create datasets for cvh and cvl
  d = fid.create('cvh', SDC.FLOAT64, (nlat, nlon))
  dim0 = d.dim(0)
  dim1 = d.dim(1)
  dim0.setname('LAT')
  dim1.setname('LON')
  d[:] = cvh
  d.endaccess()
  
  d = fid.create('cvl', SDC.FLOAT64, (nlat, nlon))
  dim0 = d.dim(0)
  dim1 = d.dim(1)
  dim0.setname('LAT')
  dim1.setname('LON')
  d[:] = cvl
  d.endaccess()
  
  # Add variable attributes the same as in tm5 veg 2009 raw file
  ds_names = fid.datasets()
  ds_raw = fid_raw.select('tv01')
  for dn in ds_names:
    ds = fid.select(dn)
    if not ds.iscoordvar():
      for attr_name, attr_value in ds_raw.attributes().items():
        setattr(ds, attr_name, attr_value)
  
  # Close file
  fid.end()
  # fid_raw.end()
  
  # Check file info
  fid, fattr, fdset = pf.h4dump(fname, verb, output)

  return fid, fattr, fdset
