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
import os
import sys
sys.path.insert(0, '/homeappl/home/putian/scripts/science-helper/pypack')

# import netCDF4 as netcdf
from netCDF4 import Dataset

import numpy as np

import lu2018
from local import *


def read_data():
  print('Reading Lu2018 data for PI ...')
  df_lu2018[case_list[0]] = lu2018.Lu2018(dir_lu2018_data + '/' + file_list[0])

  print('Reading Lu2018 data for MH ...')
  df_lu2018[case_list[1]] = lu2018.Lu2018(dir_lu2018_data + '/' + file_list[1])

  print('Reading Lu2018 data for MHgsrd ...')
  df_lu2018[case_list[2]] = lu2018.Lu2018(dir_lu2018_data + '/' + file_list[2])

  return df_lu2018


#==============================================================================#
#
# Interpolate the scattered data to regular lon-lat coordinates
#
# Now the bi-linear interpolation is used to get the coverage for the grid cells:
# describe the interpolation method ...
#
# 1. Read the land grid ll: lon_land, lat_land
# 2. Generate the global grid ll: lon_glob, lat_glob
# 3. Generate regular global grid for reduced Gaussian latitudes and 1 degree lat
# 4. Obtain the indices of lon and lat for each land grid in the global grid: land_ind
# 5. Interpolation:
#    (1) Loop for each latitude
#    (2) Put the land data to global grid for reduced Gaussian grid
#    (3) Interpolate every latitude from global reduced Gaussian to global regular grid
#    (4) Interpolate for every longitude in the regular grid
#
#==============================================================================#
def add_data_g11():
  # Interpolate from lrg to g11 for each case
  print('Processing PI ...')
  df_lu2018[case_list[0]].data_g11 = \
      df_lu2018[case_list[0]].calc_data_gxx(lu2018.Lu2018.lon_g11, lu2018.Lu2018.lat_g11, debug=True)
  
  print('Processing MH ...')
  df_lu2018[case_list[0]].data_g11 = \
      df_lu2018[case_list[0]].calc_data_gxx(lu2018.Lu2018.lon_g11, lu2018.Lu2018.lat_g11, debug=True)
  
  print('Processing MH_gsrd ...')
  df_lu2018[case_list[0]].data_g11 = \
      df_lu2018[case_list[0]].calc_data_gxx(lu2018.Lu2018.lon_g11, lu2018.Lu2018.lat_g11, debug=True)

  return df_lu2018
  

def save_data_g11(fname):
  # Save the data
  np.savez(fname, \
      pi =df_lu2018[case_list[0]].data_g11, \
      mh1=df_lu2018[case_list[1]].data_g11, \
      mh2=df_lu2018[case_list[2]].data_g11)


#==============================================================================#
#
# Combine the data to get the cvl, cvh and tv
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
#  8    0                0            0            0   
#  9    lu2018_mhgsrd    lu2018_mh    lu2018_pi    tm5_veg2009
# 10    0                0            0            tm5_veg2009
# 11    0                0            0            tm5_veg2009
# 12    0                0            0            0   
# 13    lu2018_mhgsrd    lu2018_mh    lu2018_pi    tm5_veg2009
# 14    0                0            0            0   
# 15    0                0            0            0   
# 16    0                0            0            tm5_veg2009
# 17    0                0            0            tm5_veg2009
# 18    lu2018_mhgsrd    lu2018_mh    lu2018_pi    tm5_veg2009
# 19    0                0            0            tm5_veg2009
# 20    0                0            0            0   
#
# tvh_all = tvh_lu2018(all high veg) + tvh_2009(all high veg)*cvh_2009
# tvl_all = tvl_lu2018(all low veg) + tvl_2009(all low veg)*cvl_2009
#
# So we do not need to change the values from Lu2018, we can just use them
#
#==============================================================================#


#==============================================================================#
#
# Main program
#
#==============================================================================#
if __name__ == '__main__':
  #
  # Modify onlinedust wrt to meteo veg
  #

  potsrc_region = [10.0, 30.0, -20.0, 40.0]
  soilph_threshold = 0.2

  # Cultivation is 0 for pi, mh1, and mh2
  cult_new = 0

  # year_str = '1859'
  year_str = '1850_1859_mean'

  for c in case_list:

    #
    # cvl and cvh
    # [last year (1859), all months, lon, lat] --> annual mean [lat, lon]
    #
    fid_lu2018_veg_gxx = Dataset(get_fname_lu2018_veg_gxx(c), 'r')

    # cvl
    cvl_annual_mean = np.mean(fid_lu2018_veg_gxx.variables['cvl'][:, :, :, :], axis = (0, 1))
    print(cvl_annual_mean.shape)
    cvl = np.transpose(cvl_annual_mean)

    # cvh
    cvh_annual_mean = np.mean(fid_lu2018_veg_gxx.variables['cvh'][:, :, :, :], axis = (0, 1))
    print(cvh_annual_mean.shape)
    cvh = np.transpose(cvh_annual_mean)

    modify_onlinedust_from_veg(get_fname_sample_dust(), get_fname_new_dust(c, year_str), \
      cvl, cvh, \
      potsrc_region, cult_new, soilph_threshold)
