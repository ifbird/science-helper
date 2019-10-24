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

#
# Raw Lu2018 BVOC data files
#

# Lu2018 BVOC lpjg data file names of iso(prene) and mon(oterpenes) in nc format
fname_lu2018_iso = {}
fname_lu2018_mon = {}
for c in case_list:
  fname_lu2018_iso[c] = get_fname_lu2018_gxx(c, 'iso')
  fname_lu2018_mon[c] = get_fname_lu2018_gxx(c, 'mon')


#
# Raw MEGAN emission data file name as a sample
#

fdir_megan_sample = '/proj/atm/TM5_EMISS/MEGAN'
fname_megan_sample_iso = get_fname_megan_sample('iso', '2009')
fname_megan_sample_mon = get_fname_megan_sample('mon', '2009')


#
# Generated MEGAN emission data file names for iso and mon
# This will be created later.
#


#==============================================================================#
# Helper functions
#==============================================================================#
def create_megan_new_file_from_lu2018_bvoc_data_gxx(data_gxx_lu2018_bvoc, fname_megan_sample, fname_megan_new):
  """
  " data_gxx_lu2018_bvoc: 1-year data at gxx grid, should be (date, lat, lon)
  " fname_megan_sample: sample file name
  " fname_megan_new_: new input data file name
  """
  # Sample MEGAN emission data
  fid_megan_sample, fattrs_megan_sample, fdims_megan_sample, fvars_megan_sample= \
    netcdf.ncdump(fname_megan_sample, verb=False, log_file='megan_sample.txt')

  # Create a new netcdf file to save the interpolated data
  fid_megan_new = Dataset(fname_megan_new, 'w')
  
  # Copy global attributes from sample files
  netcdf.copy_global_attributes(fid_megan_sample, fid_megan_new)
  
  # Copy dimensions
  for dname in fdims_megan_sample:
    netcdf.copy_dimension(fid_megan_sample, fid_megan_new, dname)
      
  # Copy variables except vname
  netcdf.copy_variable(fid_megan_sample, fid_megan_new, 'lon')
  netcdf.copy_variable(fid_megan_sample, fid_megan_new, 'lat')
  netcdf.copy_variable(fid_megan_sample, fid_megan_new, 'date')
  netcdf.copy_variable(fid_megan_sample, fid_megan_new, 'MEGAN_MACC')

  # Copy the Lu2018 BVOC data to the new nc files
  MEGAN_MACC = fid_megan_new.variables['MEGAN_MACC']
  for i in range(ndate):
    MEGAN_MACC[:] = data_gxx_lu2018_bvoc

  # Close files
  fid_megan_sample.close()
  fid_megan_new.close()


#==============================================================================#
# Main program
#==============================================================================#
if __name__=='__main__':
  #
  # Read data
  #

  data_gxx_lu2018_iso = {}
  data_gxx_lu2018_mon = {}
  fid_lu2018_iso = {}
  fid_lu2018_mon = {}
  for c in case_list:
    fid_lu2018_iso[c] = Dataset(fname_lu2018_iso[c], 'r')
    fid_lu2018_mon[c] = Dataset(fname_lu2018_mon[c], 'r')

    data_gxx_lu2018_iso[c] = fid_lu2018_iso[c].variables['data_gxx'][:]
    data_gxx_lu2018_mon[c] = fid_lu2018_mon[c].variables['data_gxx'][:]

    # Convert the unit: [mg m-2 mon-1] --> [kg m-2 s-1]
    for im in range(nmon):
      data_gxx_lu2018_iso[c][:, im, :, :] *= unit_conv(68.0e-3, month_day[im])
      data_gxx_lu2018_mon[c][:, im, :, :] *= unit_conv(136.0e-3, month_day[im])

  #
  # Save the data
  #
  for c in case_list:
    for iy in range(nyear):  # loop from 1850 to 1859
      print('Saving data of {0} in {1} ...'.format(c, 1850+iy))

      # isoprene
      print('Isoprene')
      data_tmp = np.transpose( data_gxx_lu2018_iso[c][iy][:, :, :], (0, 2, 1) )
      fname_megan_new = get_fname_megan_new(c, 'iso', '{0:4d}'.format(1850+iy))
      create_megan_new_file_from_lu2018_bvoc_data_gxx(data_tmp, fname_megan_sample_iso, fname_megan_new)

      # Monoterpenes
      print('Monoterpenes')
      data_tmp = np.transpose( data_gxx_lu2018_mon[c][iy][:, :, :], (0, 2, 1) )
      fname_megan_new = get_fname_megan_new(c, 'mon', '{0:4d}'.format(1850+iy))
      create_megan_new_file_from_lu2018_bvoc_data_gxx(data_tmp, fname_megan_sample_mon, fname_megan_new)

    # Also generate a mean field data file

    # isoprene
    print('Saving 10-year mean isoprene data ...')
    data_tmp = np.transpose( np.squeeze(np.mean(data_gxx_lu2018_iso[c], axis=0)), (0, 2, 1) )
    fname_megan_new = fdir_megan_new + '/{0}-MEGAN-MACC_biogenic_1850_1859_mean_isoprene.nc'.format(c)
    fname_megan_new = get_fname_megan_new(c, 'iso', '1850_1859_mean')
    create_megan_new_file_from_lu2018_bvoc_data_gxx(data_tmp, fname_megan_sample_iso, fname_megan_new)

    # Monoterpenes
    print('Saving 10-year mean monoterpenes data ...')
    data_tmp = np.transpose( np.squeeze(np.mean(data_gxx_lu2018_mon[c], axis=0)), (0, 2, 1) )
    fname_megan_new = get_fname_megan_new(c, 'mon', '1850_1859_mean')
    create_megan_new_file_from_lu2018_bvoc_data_gxx(data_tmp, fname_megan_sample_mon, fname_megan_new)
