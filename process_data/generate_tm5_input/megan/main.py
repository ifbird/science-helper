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
fname_lu2018_iso['pi' ] = fdir_lu2018_bvoc_case['pi' ] + '/miso_1850_1859_gxx.nc'
fname_lu2018_iso['mh1'] = fdir_lu2018_bvoc_case['mh1'] + '/miso_1850_1859_gxx.nc'
fname_lu2018_iso['mh2'] = fdir_lu2018_bvoc_case['mh2'] + '/miso_1850_1859_gxx.nc'

fname_lu2018_mon = {}
fname_lu2018_mon['pi' ] = fdir_lu2018_bvoc_case['pi' ] + '/mmon_1850_1859_gxx.nc'
fname_lu2018_mon['mh1'] = fdir_lu2018_bvoc_case['mh1'] + '/mmon_1850_1859_gxx.nc'
fname_lu2018_mon['mh2'] = fdir_lu2018_bvoc_case['mh2'] + '/mmon_1850_1859_gxx.nc'


#
# Raw MEGAN emission data file name as a sample
#

# fdir_megan_sample = '/homeappl/home/putian/scripts/tm5-mp/data/lu2018_lpjg_monthly_bvoc/tm5_megan_input_sample/'
# fname_megan_sample_iso = fdir_megan_sample + '/MEGAN-MACC_biogenic_2005_isoprene.nc'
# fname_megan_sample_mon = fdir_megan_sample + '/MEGAN-MACC_biogenic_2005_monoterpenes.nc'

fdir_megan_sample = '/proj/atm/TM5_EMISS/MEGAN'
fname_megan_sample_iso = fdir_megan_sample + '/MEGAN-MACC_biogenic_2009_isoprene.nc'
fname_megan_sample_mon = fdir_megan_sample + '/MEGAN-MACC_biogenic_2009_monoterpenes.nc'

#
# Generated MEGAN emission data file name
#

# Folder
fdir_megan_new = '/homeappl/home/putian/scripts/tm5-mp/data/tm5_input_modified/megan'

# Modified files for iso and mon
fname_megan_new_iso = {}
fname_megan_new_iso['pi'] = fdir_megan_new + '/MEGAN-MACC_biogenic_pi_isoprene.nc'
fname_megan_new_iso['mh1'] = fdir_megan_new + '/MEGAN-MACC_biogenic_mh1_isoprene.nc'
fname_megan_new_iso['mh2'] = fdir_megan_new + '/MEGAN-MACC_biogenic_mh2_isoprene.nc'

fname_megan_new_mon = {}
fname_megan_new_mon['pi'] = fdir_megan_new + '/MEGAN-MACC_biogenic_pi_monoterpenes.nc'
fname_megan_new_mon['mh1'] = fdir_megan_new + '/MEGAN-MACC_biogenic_mh1_monoterpenes.nc'
fname_megan_new_mon['mh2'] = fdir_megan_new + '/MEGAN-MACC_biogenic_mh2_monoterpenes.nc'

# Case list
case_list = ['pi', 'mh1', 'mh2']

# Year count in Lu2018 BVOC data
nyear = 10
nmon = 12; ndate = nmon


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
  
  # Copy dimensions except
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

  # Interpolated Lu2018 BVOC data (done in 'preprocess.py')
  data_gxx_lu2018_iso = {}
  data_gxx_lu2018_mon = {}
  fid_lu2018_iso = {}
  fid_lu2018_mon = {}
  for c in case_list:
    fid_lu2018_iso[c] = Dataset(fname_lu2018_iso[c], 'r')
    fid_lu2018_mon[c] = Dataset(fname_lu2018_mon[c], 'r')

    data_gxx_lu2018_iso[c] = fid_lu2018_iso[c].variables['data_gxx'][:]
    data_gxx_lu2018_mon[c] = fid_lu2018_mon[c].variables['data_gxx'][:]

  #
  # Save the data
  #
  for c in case_list:
    for iy in range(nyear):  # loop from 1850 to 1859
      print('Saving data of {0} in {1} ...'.format(c, 1850+iy))

      # isoprene
      print('Isoprene')
      data_tmp = np.transpose( data_gxx_lu2018_iso[c][iy][:, :, :], (0, 2, 1) )
      fname_megan_new = fdir_megan_new + '/MEGAN-MACC_biogenic_{0}_{1:4d}_isoprene.nc'.format(c, 1850+iy)
      create_megan_new_file_from_lu2018_bvoc_data_gxx(data_tmp, fname_megan_sample_iso, fname_megan_new)

      # Monoterpenes
      print('Monoterpenes')
      data_tmp = np.transpose( data_gxx_lu2018_mon[c][iy][:, :, :], (0, 2, 1) )
      fname_megan_new = fdir_megan_new + '/MEGAN-MACC_biogenic_{0}_{1:4d}_monoterpenes.nc'.format(c, 1850+iy)
      create_megan_new_file_from_lu2018_bvoc_data_gxx(data_tmp, fname_megan_sample_mon, fname_megan_new)

    # Also generate a mean field data file

    # isoprene
    print('Saving 10-year mean isoprene data ...')
    data_tmp = np.transpose( np.squeeze(np.mean(data_gxx_lu2018_iso[c], axis=0)), (0, 2, 1) )
    fname_megan_new = fdir_megan_new + '/MEGAN-MACC_biogenic_{0}_1850_1859_mean_isoprene.nc'.format(c)
    create_megan_new_file_from_lu2018_bvoc_data_gxx(data_tmp, fname_megan_sample_iso, fname_megan_new)

    # Monoterpenes
    print('Saving 10-year mean monoterpenes data ...')
    data_tmp = np.transpose( np.squeeze(np.mean(data_gxx_lu2018_mon[c], axis=0)), (0, 2, 1) )
    fname_megan_new = fdir_megan_new + '/MEGAN-MACC_biogenic_{0}_1850_1859_mean_monoterpenes.nc'.format(c)
    create_megan_new_file_from_lu2018_bvoc_data_gxx(data_tmp, fname_megan_sample_mon, fname_megan_new)
