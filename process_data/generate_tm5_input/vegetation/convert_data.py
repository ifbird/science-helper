"""
"
" Readme
"
" Read original Lu2018 vegetation data and then interpolate them to 1.0x1.0 grid data.
" Then save the interpolated data to netcdf file for future use.
"
" LPJ-GUESS_monthlyoutput_PI.txt     --> pi-lpjg_monthly_gxx.nc
" LPJ-GUESS_monthlyoutput_MH.txt     --> mh1-lpjg_monthly_gxx.nc
" LPJ-GUESS_monthlyoutput_MHgsrd.txt --> mh2-lpjg_monthly_gxx.nc
"
" Variables saved:
"   year: 1850, 1851, ..., 1859
"   mon: 1, 2, ..., 12
"   lon, lat: 1.0x1.0 the same as in meteo veg input files
"   data_gxx: interpolated data at 1.0x1.0 grid
"
"""


#==============================================================================#
# Header
#==============================================================================#

import os
import sys
sys.path.insert(0, '/homeappl/home/putian/scripts/science-helper/pypack')

import numpy as np
from netCDF4 import Dataset

import lu2018
import netcdf
from local import *


#==============================================================================#
# Set parameters
#==============================================================================#

# Lu2018 vegetation data files
fname_lu2018_veg_lrg = {}
for c in case_list:
  fname_lu2018_veg_lrg[c] = get_fname_lu2018_veg_lrg(c)


# New netcdf files
fname_lu2018_veg_gxx = {}
for c in case_list:
  fname_lu2018_veg_gxx[c] = get_fname_lu2018_veg_gxx(c)


# Meteo vegetation sample files
fname_sample_veg = get_fname_sample_veg('2009', '01', '01')


#==============================================================================#
# Main program
#==============================================================================#
#
# Read data
#

# Raw Lu2018 veg data
data_lu2018_veg_lrg = {}
for c in case_list:
  data_lu2018_veg_lrg[c] = lu2018.Lu2018(fname_lu2018_veg_lrg[c])

# Meteo veg sample data
fid_sample_veg, fattrs_sample_veg, fdims_sample_veg, fvars_sample_veg = \
  netcdf.ncdump(fname_sample_veg, verb=False, log_file='sample_veg.txt')

# Get the dimension variables from sample file
lon_gxx = fid_sample_veg.variables['lon'][:].filled();  # masked array to normal one
lat_gxx = fid_sample_veg.variables['lat'][:].filled();  # masked array to normal one

#
# Interpolate and save the data to netcdf files
#

for c in case_list:
  # Interpolate data from lrg to gxx
  print('Interpolating data {0} ...'.format(c))
  data_lu2018_veg_lrg[c].calc_data_gxx(lon_gxx, lat_gxx, debug=True)

  # Save the data
  print('Saving data to {0} ...'.format(c))
  data_lu2018_veg_lrg[c].save_data_gxx_to_netcdf(fname_lu2018_veg_gxx[c])
