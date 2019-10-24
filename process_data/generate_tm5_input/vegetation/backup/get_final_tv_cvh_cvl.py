#==============================================================================#
#
# Prepare the input data for MH simulation with TM5-MP.
#
# Vegetation input
#
# Online dust input
#
#==============================================================================#

#
# Import header
#
import sys

import netCDF4 as netcdf

import numpy as np
import numpy.ma as ma

from mpl_toolkits.basemap import Basemap
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy.interpolate import griddata

import putian_functions as pf
import local_functions as lf

#
# Read data from npz data file
#

# data1_reg11.npz: lu2018_pi, lu2018_mh, lu2018_mhgsrd
data1 = np.load('data1_reg11.npz')

# data2_tm5veg_200902.npz: tv, cvh, cvl, lat, lon
data2 = np.load('data2_tm5veg_200902.npz')


#
# Prepare the data
#

# Dominant monthly average at regular 1x1 grid in Feb from Lu2018
# Here tv is actually the coverage: vegetation area / grid area
# tv: 0 - 1 --> 0 - 100 to be consistent with tm5 veg data
# Set the latitude to from south to north to be the same as tm5 veg 2009
tv_pi     = data1['lu2018_pi'    ][()]['tv_dom_reg11']
tv_mh     = data1['lu2018_mh'    ][()]['tv_dom_reg11']
tv_mhgsrd = data1['lu2018_mhgsrd'][()]['tv_dom_reg11']

cvl_pi     = data1['lu2018_pi'    ][()]['cvl_dom_avg_reg11']
cvl_mh     = data1['lu2018_mh'    ][()]['cvl_dom_avg_reg11']
cvl_mhgsrd = data1['lu2018_mhgsrd'][()]['cvl_dom_avg_reg11']

cvh_pi     = data1['lu2018_pi'    ][()]['cvh_dom_avg_reg11']
cvh_mh     = data1['lu2018_mh'    ][()]['cvh_dom_avg_reg11']
cvh_mhgsrd = data1['lu2018_mhgsrd'][()]['cvh_dom_avg_reg11']

lon_lu2018 = data1['lu2018_pi'][()]['lon_reg11']
lat_lu2018 = data1['lu2018_pi'][()]['lat_reg11']  # -89.5, -88.5, ..., 89.5


# tv, cvh, cvl from tm5 veg input data in Feb, 2009
# tv: 0 - 100
# cvh: 0 - 1
# cvl: 0 - 1
tv_2009 = data2['tv']
cvh_2009 = data2['cvh']
cvl_2009 = data2['cvl']
lon_2009 = data2['lon']
lat_2009 = data2['lat']

# They should have the same lon and lat
lon, lat = lon_2009, lat_2009
nlon, nlat = lon.size, lat.size


def get_input_from_lu2018_and_tm5veg_new(tv_lu2018, cvl_lu2018, cvh_lu2018, lat, lon):
  # Get number of lat and lon
  # nlat, nlon = lat.size, lon.size

  # Initiate input data dict
  input_veg = {}

  # Set lat and lon
  input_veg['lat'] = lat
  input_veg['lon'] = lon

  # Set tv according to lu2018
  input_veg['tv'] = tv_lu2018

  # Set cvl and cvh from lu2018
  input_veg['cvl'] = cvl_lu2018
  input_veg['cvh'] = cvh_lu2018

  return input_veg


#
# Combine the data
#
# In tm5, for high veg i:
#   tv[i] = area of veg i / area of total high veg * 100
# For low veg i:
#   tv[i] = area of veg i / area of total low veg * 100
# cvh = high veg area / grid area
# cvl = low veg area / grid area
#
#       MH_gsrd          MH           1850         2009
#  1    0                0            0            tm5_veg2009
#  2    lu2018_mhgsrd    lu2018_mh    lu2018_pi    tm5_veg2009
#  3    lu2018_mhgsrd    lu2018_mh    lu2018_pi    tm5_veg2009
#  4    lu2018_mhgsrd    lu2018_mh    lu2018_pi    tm5_veg2009
#  5    lu2018_mhgsrd    lu2018_mh    lu2018_pi    tm5_veg2009
#  6    lu2018_mhgsrd    lu2018_mh    lu2018_pi    tm5_veg2009
#  7    lu2018_mhgsrd    lu2018_mh    lu2018_pi    tm5_veg2009
#  8    None             None         None         None
#  9    lu2018_mhgsrd    lu2018_mh    lu2018_pi    tm5_veg2009
# 10    0                0            0            tm5_veg2009
# 11    tm5_veg2009      tm5_veg2009  tm5_veg2009  tm5_veg2009
# 12    None             None         None         None
# 13    lu2018_mhgsrd    lu2018_mh    lu2018_pi    tm5_veg2009
# 14    None             None         None         None
# 15    None             None         None         None
# 16    tm5_veg2009      tm5_veg2009  tm5_veg2009  tm5_veg2009
# 17    tm5_veg2009      tm5_veg2009  tm5_veg2009  tm5_veg2009
# 18    lu2018_mhgsrd    lu2018_mh    lu2018_pi    tm5_veg2009
# 19    tm5_veg2009      tm5_veg2009  tm5_veg2009  tm5_veg2009
# 20    None             None         None         None
#
# tvh_all = tvh_lu2018(all high veg) + tvh_2009(all high veg)*cvh_2009
# tvl_all = tvl_lu2018(all low veg) + tvl_2009(all low veg)*cvl_2009
#

def get_input_from_lu2018_and_tm5veg(tv_lu2018, tv_tm5veg, cvh_tm5veg, cvl_tm5veg, lat, lon):
  # Get number of lat and lon
  nlat, nlon = lat.size, lon.size

  # Initiate input data dict
  input_veg = {}

  input_veg['tv'] = np.zeros((lf.nvt, nlat, nlon))
  input_veg['cvh'] = np.zeros((nlat, nlon))
  input_veg['cvl'] = np.zeros((nlat, nlon))
  input_veg['lat'] = lat
  input_veg['lon'] = lon

  # Obtain data from lu2018
  ivt_lu2018 = [2, 3, 4, 5, 6, 7, 9, 13, 18]
  for i in ivt_lu2018:
    ind = int(i-1)
    input_veg['tv'][ind, :, :] = tv_lu2018[ind, :, :]

  # Obtain data from tm5 veg
  ivt_tm5veg = [11, 16, 17, 19]
  for i in ivt_tm5veg:
    ind = int(i-1)
    # input_veg['tv'][ind, :, :] = tv_tm5veg[ind, :, :]
    if lf.tm5_veglh[ind] == 'H':
      input_veg['tv'][ind, :, :] = tv_tm5veg[ind, :, :]*cvh_tm5veg[:, :] # * lf.tm5_cveg[ind]
    elif lf.tm5_veglh[ind] == 'L':
      input_veg['tv'][ind, :, :] = tv_tm5veg[ind, :, :]*cvl_tm5veg[:, :] # * lf.tm5_cveg[ind]

  # cvh, cvl
  input_veg['cvh'] = np.sum( input_veg['tv'][lf.tm5_veg_high-1, :, :], axis=0 ) / 100.0
  input_veg['cvl'] = np.sum( input_veg['tv'][lf.tm5_veg_low-1 , :, :], axis=0 ) / 100.0

  # Calculate the vegetation percentage
  eps = 1.0e-30  # avoid divided by zero
  input_veg['tv'][lf.tm5_veg_high-1, :, :] = input_veg['tv'][lf.tm5_veg_high-1, :, :] / (input_veg['cvh'][np.newaxis, :, :] + eps)
  input_veg['tv'][lf.tm5_veg_low -1, :, :] = input_veg['tv'][lf.tm5_veg_low -1, :, :] / (input_veg['cvl'][np.newaxis, :, :] + eps)

  input_veg['cvh'] = np.minimum( input_veg['cvh'], 1.0 )
  input_veg['cvl'] = np.minimum( input_veg['cvl'], 1.0 )

  return input_veg


# Old set up
# input_pi     = get_input_from_lu2018_and_tm5veg(tv_pi    , tv_2009, cvh_2009, cvl_2009, lat, lon)
# input_mh     = get_input_from_lu2018_and_tm5veg(tv_mh    , tv_2009, cvh_2009, cvl_2009, lat, lon)
# input_mhgsrd = get_input_from_lu2018_and_tm5veg(tv_mhgsrd, tv_2009, cvh_2009, cvl_2009, lat, lon)

# New set up
# print(tv_pi.shape, cvl_pi.shape, cvh_pi.shape)
input_pi     = get_input_from_lu2018_and_tm5veg_new(tv_pi    , np.nanmean(cvl_pi, axis=0)    , np.nanmean(cvh_pi, axis=0)    , lat, lon)
input_mh     = get_input_from_lu2018_and_tm5veg_new(tv_mh    , np.nanmean(cvl_mh, axis=0)    , np.nanmean(cvh_mh, axis=0)    , lat, lon)
input_mhgsrd = get_input_from_lu2018_and_tm5veg_new(tv_mhgsrd, np.nanmean(cvl_mhgsrd, axis=0), np.nanmean(cvh_mhgsrd, axis=0), lat, lon)

# print(np.max(tv_2009), np.min(tv_2009))
# print(np.max(cvh_2009), np.min(cvh_2009))
# print(np.max(cvl_2009), np.min(cvl_2009))
# print(np.max(input_pi['tv']), np.min(input_pi['tv']))
# print(np.max(input_mh['tv']), np.min(input_mh['tv']))
# print(np.max(input_mhgsrd['tv']), np.min(input_mhgsrd['tv']))

#
# Save the data
#
print('Saving data3_input.npz ...')
np.savez('data3_input.npz', input_pi=input_pi, input_mh=input_mh, input_mhgsrd=input_mhgsrd)


sys.exit()


# Initiate input data
print('Initiate input data ...')

input_pi = {}
input_mh = {}
input_mhgsrd = {}

for d in (input_pi, input_mh, input_mhgsrd):
  d['tv'] = np.zeros((lf.nvt, nlat, nlon))
  d['cvh'] = np.zeros((nlat, nlon))
  d['cvl'] = np.zeros((nlat, nlon))

  # lat and lon
  d['lat'] = lat_lu2018
  d['lon'] = lon_lu2018

##### PI
print('Calculate tv, cvh, cvl for PI ...')

# lu2018_pi
for i in (2, 3, 4, 5, 6, 7, 9, 13, 18):
  ind = int(i-1)
  input_pi['tv'][ind, :, :] = tv_pi[ind, :, :]

# tm5_veg2009
for i in (11, 16, 17, 19):
  ind = int(i-1)
  if lf.tm5_veglh[ind] == 'H':
    input_pi['tv'][ind, :, :] = tv_2009[ind, :, :]*cvh_2009[:, :]
  elif lf.tm5_veglh[ind] == 'L':
    input_pi['tv'][ind, :, :] = tv_2009[ind, :, :]*cvl_2009[:, :]
  else:  # default value 0
    pass

# tvh_all, tvl_all
input_pi['cvh'] = np.sum( input_pi['tv'][lf.tm5_veg_high-1, :, :], axis=0 )
input_pi['cvl'] = np.sum( input_pi['tv'][lf.tm5_veg_low-1 , :, :], axis=0 )

# Calculate the vegetation percentage
input_pi['tv'][lf.tm5_veg_high-1, :, :] /= input_pi['cvh'][np.newaxis, :, :]
input_pi['tv'][lf.tm5_veg_low-1 , :, :] /= input_pi['cvl'][np.newaxis, :, :]
input_pi['tv'] *= 100.0


##### MH
print('Calculate tv, cvh, cvl for MH ...')

# lu2018_pi
for i in (2, 3, 4, 5, 6, 7, 9, 13, 18):
  ind = int(i-1)
  input_mh['tv'][ind, :, :] = tv_mh[ind, :, :]

# tm5_veg2009
for i in (11, 16, 17, 19):
  ind = int(i-1)
  if lf.tm5_veglh[ind] == 'H':
    input_mh['tv'][ind, :, :] = tv_2009[ind, :, :]*cvh_2009[:, :]
  elif lf.tm5_veglh[ind] == 'L':
    input_mh['tv'][ind, :, :] = tv_2009[ind, :, :]*cvl_2009[:, :]
  else:  # default value 0
    pass

# tvh_all, tvl_all
input_mh['cvh'] = np.sum( input_mh['tv'][lf.tm5_veg_high-1, :, :], axis=0 )
input_mh['cvl'] = np.sum( input_mh['tv'][lf.tm5_veg_low-1 , :, :], axis=0 )

# Calculate the vegetation percentage
input_mh['tv'][lf.tm5_veg_high-1, :, :] /= input_mh['cvh'][np.newaxis, :, :]
input_mh['tv'][lf.tm5_veg_low-1 , :, :] /= input_mh['cvl'][np.newaxis, :, :]
input_mh['tv'] *= 100.0


##### MH_gsrd
print('Calculate tv, cvh, cvl for MH_gsrd ...')

# lu2018_pi
for i in (2, 3, 4, 5, 6, 7, 9, 13, 18):
  ind = int(i-1)
  input_mhgsrd['tv'][ind, :, :] = tv_mhgsrd[ind, :, :]

# tm5_veg2009
for i in (11, 16, 17, 19):
  ind = int(i-1)
  if lf.tm5_veglh[ind] == 'H':
    input_mh['tv'][ind, :, :] = tv_2009[ind, :, :]*cvh_2009[:, :]
  elif lf.tm5_veglh[ind] == 'L':
    input_mh['tv'][ind, :, :] = tv_2009[ind, :, :]*cvl_2009[:, :]
  else:  # default value 0
    pass

# tvh_all, tvl_all
input_mhgsrd['cvh'] = np.sum( input_mhgsrd['tv'][lf.tm5_veg_high-1, :, :], axis=0 )
input_mhgsrd['cvl'] = np.sum( input_mhgsrd['tv'][lf.tm5_veg_low-1 , :, :], axis=0 )

# Calculate the vegetation percentage
input_mhgsrd['tv'][lf.tm5_veg_high-1, :, :] /= input_mhgsrd['cvh'][np.newaxis, :, :]
input_mhgsrd['tv'][lf.tm5_veg_low-1 , :, :] /= input_mhgsrd['cvl'][np.newaxis, :, :]
input_mhgsrd['tv'] *= 100.0


#
# Save the data
#
np.savez('data3_input.npz', input_pi=input_pi, input_mh=input_mh, input_mhgsrd=input_mhgsrd)
