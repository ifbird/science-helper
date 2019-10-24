"""
"
" Readme
"
" Read original Lu2018 vegetation data and then interpolate them to 0.5x0.5 grid data.
" Then save the interpolated data to netcdf file for future use.
"
" miso_1850_1859.txt --> miso_1850_1859_gxx.nc
" mmon_1850_1859.txt --> mmon_1850_1859_gxx.nc
"
" Variables saved:
"   year: 1850, 1851, ..., 1859
"   mon: 1, 2, ..., 12
"   lon, lat: 0.5x0.5 the same as in megan sample input files
"   data_gxx: interpolated data at 0.5x0.5 grid
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


#==============================================================================#
# Set parameters
#==============================================================================#

#
# Raw Lu2018 BVOC data files
#

# Folder
fdir_lu2018_bvoc = '/homeappl/home/putian/scripts/tm5-mp/data/lu2018_lpjg_monthly_bvoc/'
fdir_lu2018_bvoc_case = {}
fdir_lu2018_bvoc_case['pi' ] = fdir_lu2018_bvoc + '/out_bvoc_pi'
fdir_lu2018_bvoc_case['mh1'] = fdir_lu2018_bvoc + '/out_bvoc_mh1'
fdir_lu2018_bvoc_case['mh2'] = fdir_lu2018_bvoc + '/out_bvoc_mh2'

# Lu2018 BVOC lpjg data file names of iso(prene) and mon(oterpenes)
fname_lu2018_iso = {}
fname_lu2018_iso['pi' ] = fdir_lu2018_bvoc_case['pi' ] + '/miso_1850_1859.txt'
fname_lu2018_iso['mh1'] = fdir_lu2018_bvoc_case['mh1'] + '/miso_1850_1859.txt'
fname_lu2018_iso['mh2'] = fdir_lu2018_bvoc_case['mh2'] + '/miso_1850_1859.txt'

fname_lu2018_mon = {}
fname_lu2018_mon['pi' ] = fdir_lu2018_bvoc_case['pi' ] + '/mmon_1850_1859.txt'
fname_lu2018_mon['mh1'] = fdir_lu2018_bvoc_case['mh1'] + '/mmon_1850_1859.txt'
fname_lu2018_mon['mh2'] = fdir_lu2018_bvoc_case['mh2'] + '/mmon_1850_1859.txt'


#
# Raw MEGAN emission data file name as a sample
#

fdir_megan_sample = '/proj/atm/TM5_EMISS/MEGAN'
fname_megan_sample_iso = fdir_megan_sample + '/MEGAN-MACC_biogenic_2009_isoprene.nc'
fname_megan_sample_mon = fdir_megan_sample + '/MEGAN-MACC_biogenic_2009_monoterpenes.nc'


# Case list
case_list = ['pi', 'mh1', 'mh2']


#==============================================================================#
# Main program
#==============================================================================#
if __name__=='__main__':
  #
  # Read data
  #

  # Raw Lu2018 BVOC data
  data_lu2018_iso = {}
  data_lu2018_mon = {}
  for c in case_list:
    data_lu2018_iso[c] = lu2018.Lu2018Bvoc(fname_lu2018_iso[c])
    data_lu2018_mon[c] = lu2018.Lu2018Bvoc(fname_lu2018_mon[c])

  # Raw MEGAN emission data
  fid_megan_sample_iso, fattrs_megan_sample_iso, fdims_megan_sample_iso, fvars_megan_sample_iso = \
    netcdf.ncdump(fname_megan_sample_iso, verb=True, log_file='megan_sample_iso.txt')
  fid_megan_sample_iso.set_always_mask(False)  # do not convert array to masked array
  fid_megan_sample_mon, fattrs_megan_sample_mon, fdims_megan_sample_mon, fvars_megan_sample_mon = \
    netcdf.ncdump(fname_megan_sample_mon, verb=True, log_file='megan_sample_mon.txt')
  fid_megan_sample_iso.set_always_mask(False)  # do not convert array to masked array

  # Get the dimension variables from sample file
  lon_gxx = fid_megan_sample_iso.variables['lon'][:];
  lat_gxx = fid_megan_sample_iso.variables['lat'][:];
  date    = fid_megan_sample_iso.variables['date'][:]; ndate = len(date)
  nyear = 10
  
  #
  # Interpolate and save the data to netcdf files
  #

  for c in case_list:
    # Interpolate data from lrg to gxx
    print('Interpolating data {0} ...'.format(c))
    data_lu2018_iso[c].calc_data_gxx(lon_gxx, lat_gxx, debug=True)
    data_lu2018_mon[c].calc_data_gxx(lon_gxx, lat_gxx, debug=True)

    # Save the data
    print('Saving data to {0} ...'.format(c))
    fname_lu2018_netcdf_iso = fdir_lu2018_bvoc_case[c] + '/miso_1850_1859_gxx.nc'
    fname_lu2018_netcdf_mon = fdir_lu2018_bvoc_case[c] + '/mmon_1850_1859_gxx.nc'

    data_lu2018_iso[c].save_data_gxx_to_netcdf(fname_lu2018_netcdf_iso)
    data_lu2018_mon[c].save_data_gxx_to_netcdf(fname_lu2018_netcdf_mon)
